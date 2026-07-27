#BSD 3-Clause License
#
#Copyright (c) 2026, ASU-VDA-Lab
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################

"""Run KLayout design-rule checking on one crop of a layout.

Given a leaf region and its context, this module renders the crop to GDS, runs
the KLayout rule deck over it, and turns the report into JSON with the sibling
drc_postprocess module. The crop carries the full internal structure of every
instance it contains and draws top-level metal unclipped, so rules that depend
on a wire's real extent still see it. Violations on layers below V0 are then
dropped and only those whose bounding box lies entirely inside the leaf are
kept, so callers get a Counter over (rule_id, bbox) pairs rather than raw
KLayout output. The check invokes klayout directly when this process is
already inside the container image, and goes through `docker run` otherwise.
"""


import json
import os
import re
import subprocess
import tempfile
from collections import Counter

from .crop_body import (build_body, _resolve_top_cell_var, _points_for,
                        _format_points, _GDS_BY_LAYER)
from .model import instance_block_polys
from .types import LAYER_NUM_TO_NAME


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
REPAIR_IMAGE = os.environ.get("REPAIR_IMAGE", "drc-benchmark-repair")
DOCKER_API_VERSION = os.environ.get("DOCKER_API_VERSION", "1.43")
CASE_DEFAULT = "case"

# Paths the host mode mounts the work dir, rule deck, and post-processor at.
C_WORK = "/work"
C_DECK = "/deck/asap7.lydrc"
C_POST = "/post/drc_postprocess.py"


def _drc_mode():
    """Decide whether to run klayout directly or through ``docker run``.

    The presence of ``/.dockerenv`` means this process is already inside the
    repair image, so klayout can be invoked directly (``local``); otherwise it
    has to be run in a container (``docker``). Note that klayout is also
    installed on the host, so its presence on PATH says nothing about which
    mode applies. ``EVODRC_DRC_MODE`` overrides the choice.
    """
    m = os.environ.get("EVODRC_DRC_MODE", "").strip()
    if m in ("docker", "local"):
        return m
    return "local" if os.path.exists("/.dockerenv") else "docker"


# ===========================================================================
# Top-level polygon harvesting
# ===========================================================================
_RE_TOP_INSERT_TMPL = (
    r"^{TOP}\.shapes\(layout\.layer\(pya\.LayerInfo\(\s*\d+\s*,\s*\d+\s*\)\)\)"
    r"\.insert\((p\d+)\)\s*$")
_RE_POLY_DEF = re.compile(r"^(p\d+)\s*=\s*pya\.Polygon\(")


def _harvest_toplevel_pids(leaf, ctx, top_var):
    """Return the sorted ids of the top-level polygons the crop body refers to.

    The crop body is generated once and scanned for inserts into the top cell,
    which selects the editable polygons plus the read-only neighbours around
    them. Polygons that come from instances rather than the top cell are left
    out, since those are rendered separately from the cell definitions.
    """
    lines = build_body(leaf, ctx)
    top_insert_re = re.compile(_RE_TOP_INSERT_TMPL.format(TOP=re.escape(top_var)))
    top_pids = set()
    for ln in lines:
        m = top_insert_re.match(ln.strip())
        if m:
            top_pids.add(m.group(1))
    return sorted(top_pids)


# ===========================================================================
# Crop rendering
# ===========================================================================
def build_faithful_render_script(leaf, ctx, gds_path):
    """Build a KLayout script that renders the crop for DRC.

    Every instance inside the crop, via or standard cell, is emitted with its
    complete internal structure flattened into world coordinates, and every
    top-level polygon the crop body references is emitted at its original
    extent instead of being clipped to the crop window, so width and spacing
    rules see the same geometry they would in the full layout. The script ends
    with ``layout.write(gds_path)``. Returns the script text and a dict of
    counts describing what was rendered.
    """
    geom = ctx.geometry_model
    insts = geom.instances
    cell_defs = geom.cell_defs
    polys = geom.polygons
    top_var = _resolve_top_cell_var(ctx)
    case = top_var[5:] if top_var.startswith("cell_") else top_var

    out = []
    out.append("import pya")
    out.append("# faithful crop: FULL internal structure for EVERY in-crop "
               "subcell instance; top-level metal rendered FULL-LENGTH "
               "(UN-CLIPPED).")
    out.append("layout = pya.Layout()")
    out.append("layout.dbu = 0.00025")
    out.append('{0} = layout.create_cell("{1}")'.format(top_var, case))

    # Every instance inside the crop, with its internal shapes flattened into
    # world coordinates on the layer they really belong to.
    n_inst = 0
    n_poly = 0
    layers_emitted = set()
    out.append("")
    out.append("# === FULL internal structure of every in-crop subcell instance "
               "(via + std-cell), flat world coords ===")
    pk = 0
    for iid in leaf.subcell_instances:
        inst = insts.get(iid)
        if inst is None:
            continue
        wp = instance_block_polys(inst, cell_defs)
        if not wp:
            continue
        n_inst += 1
        out.append("# instance {0} ({1}, kind={2}) -- full internal structure"
                   .format(iid, inst.cell_name, inst.kind))
        for (gds, wpts, cut) in wp:
            if not wpts:
                continue
            lname = LAYER_NUM_TO_NAME.get(gds, ("V0" if gds == 18 else "L%d" % gds))
            var = "q{0}".format(pk)
            pk += 1
            out.append("{0} = pya.Polygon([{1}])".format(
                var, _format_points(wpts)))
            out.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                       ".insert({2})  # {3}".format(top_var, gds, var, lname))
            n_poly += 1
            layers_emitted.add(gds)

    # The top-level polygons the crop refers to, each drawn at its full
    # original extent so length-dependent rules behave as in the whole layout.
    top_pids = _harvest_toplevel_pids(leaf, ctx, top_var)
    out.append("")
    out.append("# === TOP-LEVEL metal polygons at FULL LENGTH (UN-CLIPPED; real "
               "original extent from geometry_model.polygons[pid]) ===")
    n_top = 0
    top_layers = set()
    skipped_pids = []
    tk = 0
    for pid in top_pids:
        poly = polys.get(pid)
        if poly is None:
            skipped_pids.append((pid, "no-poly"))
            continue
        gds = _GDS_BY_LAYER.get(poly.layer_name)
        if gds is None:
            skipped_pids.append((pid, "no-gds:%s" % poly.layer_name))
            continue
        pts = _points_for(poly)            # full outline, not clipped
        var = "t{0}".format(tk)
        tk += 1
        out.append("# top-level FULL pid={0} layer={1}".format(pid, poly.layer_name))
        out.append("{0} = pya.Polygon([{1}])".format(var, _format_points(pts)))
        out.append("{0}.shapes(layout.layer(pya.LayerInfo({1}, 0)))"
                   ".insert({2})  # {3}".format(top_var, gds, var, poly.layer_name))
        n_top += 1
        top_layers.add(poly.layer_name)

    out.append("")
    out.append("layout.write(%s)" % json.dumps(gds_path))
    text = "\n".join(out) + "\n"
    meta = {
        "n_instances_rendered": n_inst,
        "n_instance_polys": n_poly,
        "instance_layers_gds": sorted(layers_emitted),
        "n_toplevel_pids": len(top_pids),
        "n_toplevel_rendered": n_top,
        "toplevel_layers": sorted(top_layers),
        "toplevel_skipped": skipped_pids,
        "toplevel_pids": top_pids,
    }
    return text, meta


# ===========================================================================
# Below-V0 rule classification
# ===========================================================================
_DECK_INPUT_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*input\(\s*(\d+)\s*,")


def _parse_deck_layers(deck_path):
    """Return {var_name_upper: gds_num} from the deck's input() declarations."""
    layers = {}
    with open(deck_path) as fh:
        for ln in fh:
            m = _DECK_INPUT_RE.match(ln)
            if m:
                layers[m.group(1).upper()] = int(m.group(2))
    return layers


def below_v0_layer_set(deck_path):
    """Return the rule-name prefixes that belong to layers below V0.

    Repairs only touch V0 and the routing stack above it, so violations from
    the device and substrate layers underneath are not actionable. The set is
    built from the deck: every layer declared with a GDS number below V0's,
    plus the device layers that are declared with high GDS numbers, plus the
    aliases some rule families use. Returns the set of prefixes together with
    a dict describing how it was derived.
    """
    deck = _parse_deck_layers(deck_path)
    below_by_gds = {name for name, gds in deck.items() if gds < 18}
    device_high_gds = {"SDT", "SLVT", "LVT", "SRAMDRC", "SRAMVT"}
    device_high_gds = {n for n in device_high_gds if n in deck}
    aliases = {"WELL", "VT", "SRAM"}
    drop = set(below_by_gds) | set(device_high_gds) | set(aliases)
    info = {
        "below_v0_by_gds": sorted((name, deck[name]) for name in below_by_gds),
        "device_high_gds": sorted((name, deck[name]) for name in device_high_gds),
        "rule_family_aliases": sorted(aliases),
        "v0_floor_gds": deck.get("V0"),
        "keep_examples": ["V0", "M1", "V1", "M2", "V2", "M3", "..."],
        "drop_prefix_tokens": sorted(drop),
    }
    return drop, info


def rule_is_below_v0(rule_id, drop_tokens):
    """True if the rule's primary layer, the first dotted token of its id, is
    below V0."""
    first = rule_id.split(".", 1)[0].upper()
    return first in drop_tokens


# ===========================================================================
# Within-leaf restriction
# ===========================================================================
def bbox_within_leaf(viol_bbox, leaf_bbox):
    """True if viol_bbox lies entirely inside leaf_bbox, edges included."""
    vx1, vy1, vx2, vy2 = viol_bbox
    bx1, by1, bx2, by2 = leaf_bbox
    return vx1 >= bx1 and vy1 >= by1 and vx2 <= bx2 and vy2 <= by2


# ===========================================================================
# Report to multiset
# ===========================================================================
def _multiset_from_drc_json(path):
    """Counter over (rule_id, (x1,y1,x2,y2)) for a .drc.json report."""
    with open(path) as fh:
        data = json.load(fh)
    c = Counter()
    for rule, info in data.get("rules", {}).items():
        for v in info.get("violations", []):
            bb = v.get("bbox")
            if bb is None:
                continue
            c[(rule, tuple(bb))] += 1
    return c, int(data.get("total_violations", sum(c.values())))


# ===========================================================================
# DRC runner
# ===========================================================================
def _run_drc(build_render, leaf_id, case_name, design_type, rule_path,
             timeout=900):
    """Render the crop, check it, and post-process the report.

    ``build_render`` is a callable ``gds_path -> (render_text, meta)``. Passing
    the path in rather than fixing it means the render script always writes to
    the file the DRC step reads, whether that is a host path (local mode) or an
    in-container mount path (docker mode). Returns the path to the .drc.json or
    None, the working directory, and the combined log output.
    """
    mode = _drc_mode()
    if mode == "local":
        return _drc_local(build_render, leaf_id, case_name, design_type,
                          rule_path, timeout)
    return _drc_docker(build_render, leaf_id, case_name, design_type,
                       rule_path, timeout)


def _drc_local(build_render, leaf_id, case_name, design_type, rule_path,
               timeout):
    """Run the render, DRC, and post-process steps as local subprocesses."""
    work = tempfile.mkdtemp(prefix="drccheck_local_")
    gds = os.path.join(work, "%s_crop.gds" % leaf_id)
    render_text, _meta = build_render(gds)         # writes to the real gds path
    render_host = os.path.join(work, "%s_crop_render.py" % leaf_id)
    with open(render_host, "w") as fh:
        fh.write(render_text)
    lyrpt = os.path.join(work, "%s_crop.lyrpt" % leaf_id)
    drcjson = os.path.join(work, "%s_crop.drc.json" % leaf_id)
    logs = []
    try:
        # 1. render the crop to GDS
        p1 = subprocess.run(["klayout", "-b", "-r", render_host],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, timeout=timeout)
        logs.append(p1.stdout or "")
        # 2. run the rule deck, producing a .lyrpt report
        p2 = subprocess.run(["klayout", "-b", "-r", rule_path,
                            "-rd", "in_gds=" + gds,
                            "-rd", "report_file=" + lyrpt],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, timeout=timeout)
        logs.append(p2.stdout or "")
        # 3. convert the report to .drc.json
        p3 = subprocess.run(
            ["python3", "-m", "agent.src.drc_postprocess",
             "--lyrpt", lyrpt, "--output", drcjson,
             "--case_name", case_name, "--design_type", design_type,
             "--layout-script", render_host],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            universal_newlines=True, timeout=timeout)
        logs.append(p3.stdout or "")
    except subprocess.TimeoutExpired as exc:
        logs.append("TIMEOUT: " + str(exc))
    raw_log = "\n".join(logs)
    if not os.path.isfile(drcjson):
        return None, work, raw_log
    return drcjson, work, raw_log


def _drc_docker(build_render, leaf_id, case_name, design_type, rule_path,
                timeout):
    """Run the render, DRC, and post-process steps inside the repair image.

    The work directory, the rule deck, and the post-processor are bind-mounted
    into a single container that runs all three steps in one shell script.
    """
    work = tempfile.mkdtemp(prefix="drccheck_docker_")
    gds_c = "%s/%s_crop.gds" % (C_WORK, leaf_id)
    render_text, _meta = build_render(gds_c)       # writes to the in-container path
    render_host = os.path.join(work, "%s_crop_render.py" % leaf_id)
    with open(render_host, "w") as fh:
        fh.write(render_text)
    here = os.path.dirname(os.path.abspath(__file__))
    post_host = os.path.join(here, "drc_postprocess.py")

    render_c = "%s/%s_crop_render.py" % (C_WORK, leaf_id)
    lyrpt_c = "%s/%s_crop.lyrpt" % (C_WORK, leaf_id)
    drcjson_c = "%s/%s_crop.drc.json" % (C_WORK, leaf_id)

    inner = r'''
set -e
cd {W}
echo "=== render crop GDS ==="
klayout -b -r {RENDER}
echo "=== DRC (deck=asap7.lydrc) ==="
klayout -b -r {DECK} -rd in_gds={GDS} -rd report_file={LYRPT}
echo "=== vendored postprocess (.lyrpt -> .drc.json) ==="
python3 {POST} \
    --lyrpt {LYRPT} \
    --output {DRCJSON} \
    --case_name {C} \
    --design_type {DT} \
    --layout-script {RENDER}
echo "=== done ==="
'''.format(W=C_WORK, RENDER=render_c, DECK=C_DECK, GDS=gds_c, LYRPT=lyrpt_c,
           POST=C_POST, DRCJSON=drcjson_c, C=case_name, DT=design_type)

    cmd = [
        "docker", "run", "--rm",
        "-v", "%s:%s" % (work, C_WORK),
        "-v", "%s:%s:ro" % (rule_path, C_DECK),
        "-v", "%s:%s:ro" % (post_host, C_POST),
        "--entrypoint", "bash",
        REPAIR_IMAGE, "-c", inner,
    ]
    env = dict(os.environ, DOCKER_API_VERSION=DOCKER_API_VERSION)
    try:
        proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, universal_newlines=True,
                              timeout=timeout)
        raw_log = proc.stdout
    except subprocess.TimeoutExpired as exc:
        raw_log = "TIMEOUT: " + str(exc)
    drc_json = os.path.join(work, "%s_crop.drc.json" % leaf_id)
    if not os.path.isfile(drc_json):
        return None, work, raw_log
    return drc_json, work, raw_log


# ===========================================================================
# Public entry point
# ===========================================================================
def run_faithful_crop_drc(leaf, ctx, drop_tokens=None, timeout=900):
    """Check one leaf and return its violations as a multiset.

    Renders the crop, runs KLayout on it, post-processes the report, then drops
    everything below V0 and everything whose bounding box is not fully inside
    the leaf. The result is a Counter over (rule_id, (x1, y1, x2, y2)); the raw
    KLayout text survives only in the RuntimeError raised when KLayout produced
    no report at all.
    """
    info = ctx.case_info
    case_name = info.case_name or CASE_DEFAULT
    design_type = info.design_type or "block"
    rule_path = info.rule_path
    leaf_bbox = tuple(leaf.bbox_dbu)
    if drop_tokens is None:
        if rule_path and os.path.isfile(rule_path):
            drop_tokens, _ = below_v0_layer_set(rule_path)
        else:
            drop_tokens = set()

    import shutil

    def _build_render(gds_path):
        # The DRC step supplies the GDS path, so the render always writes where
        # KLayout will read.
        return build_faithful_render_script(leaf, ctx, gds_path)

    work = None
    try:
        drc_json, work, raw_log = _run_drc(
            _build_render, leaf.leaf_id, case_name, design_type, rule_path,
            timeout=timeout)
        if drc_json is None:
            raise RuntimeError("crop DRC produced no .drc.json for %s\n%s"
                               % (leaf.leaf_id, raw_log[-2000:]))
        crop_ms_raw, _total = _multiset_from_drc_json(drc_json)
    finally:
        if work is not None:
            shutil.rmtree(work, ignore_errors=True)

    crop_ms = Counter()
    for kk, c in crop_ms_raw.items():
        if rule_is_below_v0(kk[0], drop_tokens):
            continue
        if not bbox_within_leaf(kk[1], leaf_bbox):
            continue
        crop_ms[kk] += c
    return crop_ms
