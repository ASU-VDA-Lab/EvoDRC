# EvoDRC
This repository contains the experimental data from the EvoDRC paper and the executable EvoDRC framework for iteratively refining skill files during the agentic DRC repair of VLSI circuit layouts.

## Framework Description
![Inference](etc/EvoDRC.png)
Design rule check (DRC) closure remains a major bottleneck in advanced-node physical design. Although detailed routers are rule-aware, residual design rule violations (DRVs) often require manual engineering change order iterations. Automating this process is challenging because repairs must account for complex geometric interactions, preserve circuit connectivity, and avoid introducing new violations.
We present EvoDRC, a skill-evolution framework for agentic block-level DRC repair. EvoDRC initializes layer-specific repair skills using knowledge distilled from an unrelated reference design and continuously evolves these skills using traceable repair experience collected from the target design. EvoDRC decomposes the layout into bounded repair regions and assigns an LLM repair agent to each region. Local DRC analysis, connectivity-checking, and impact-preview tools provide feedback on proposed modifications. Repair operations and their resulting DRV changes are stored in a knowledge database and used to evolve the repair skills. Experiments on seven block-level designs from the DAC26 DRC Benchmark show that EvoDRC achieves a 73.5\% overall reduction compared to the reported baseline. 

## Table of content
  - [*agent/*](./agent/): EvoDRC agentic framework, replace the agent/ in DAC26_DRC_Benchmark with this
  - [*data/*](./data/): Experimental data in the paper
  - [*cla_gds/*](./cla_gds/): The external design with/without DRC
  - *DAC26_DRC_Benchmark*: The [DAC26_DRC_Benchmark](https://github.com/ASU-VDA-Lab/DAC26_DRC_Benchmark/tree/v1) repository.
  - [*external*](./external/): Copy of the initial skill file, with/without knowledge distilled from the [*cla_gds/*](./cla_gds/) case.
  - [*Dockerfile.evodrc*](./Dockerfile.evodrc): The Dockerfile used in EvoDRC.     

## EvoDRC output structure

```
data/                  Experimental data in the paper
└── <EXP>/             EvoDRC or ablation studies
    └── Block{N}/      One chip design (Block1 … Block7)
        └── <Model>/   The AI model used (claude-sonnet-4-6 with Claude Code)       
```

### The four variants (`<EXP>`)
| Folder | What is different |
|---|---|
| `evodrc` | The main method. Starts with prior experience and keeps learning. |
| `ablation1` | Starts with the rules but **no prior experience** — learns from scratch. |
| `ablation2` | Starts with experience but **never updates it** — learning is off from the first iteration onward. |
| `ablation3` | Repairs the design **as a whole** instead of splitting it into pieces. |

Comparing these four shows how much the prior experience and the continued learning
actually contribute.

### Names used in the directory tree below

| Placeholder | Meaning |
|---|---|
| `{N}` | A design number, e.g. `Block3` |
| `iter{1..N}` | An iteration — one full attempt at repairing the design |
| `<LAYER>` | A layer of the chip, e.g. `M1`–`M6` (metal) or `V0`–`V5` (vias, the connections between metal layers) |
| `<UNIT>` | One repair unit — a piece of the design handed to the agent. Named `leaf_0001` (a single piece), `Block1_union_row3` (neighbouring pieces merged), or `whole_design` (the entire design, used by `ablation3`) |

### Inside each data<EXP>/Block{N}/ folder

```
<Model>/                          The knowledge database (Knowledge DB)
│
├── usage/                        LLM cost record
│   └── iter{1..N}.jsonl          
│                                
│
├── db/                           The DB, carried across all iterations.
│   ├── main.md                   The guiding notes plus an index of everything learned.
│   ├── main_part_a.md            The original starting notes, kept unchanged for reference.
│   ├── loci.jsonl                Where each accepted repair was made in the design.
│   ├── _unmapped.jsonl           Repairs that could not be filed under any layer.
│   └── layerdb/
│       └── <LAYER>/              One folder per layer.
│           ├── rules.txt         The manufacturing rules for this layer. Written once,
│           │                     never changed.
│           ├── history.jsonl     Every attempt on this layer and how it turned out.
│           │                     Append-only — nothing is ever edited or removed.
│           └── _meta.json        When this layer's record began, plus checksums that
│                                 prove the rules were not altered.
│
├── skill/                        Provide skill files to EvoDRC in each iteration.
│   ├── <LAYER>.md                The current, best-known advice for this layer. This is
│   │                             what gets shown to the agent.
│   └── _drafts/
│       └── iterNN_<LAYER>_<VARIANT>.md
│                                 Candidate rewrites that were proposed but not adopted.
│                                 Two are written each time — one that builds on the
│                                 existing advice (`markov`), one written fresh from the
│                                 evidence alone (`stateless`) — and a separate judging
│                                 step picks at most one. Kept so the choice can be
│                                 reviewed later. Absent when learning is switched off.
│
├── crop_history/                 Crop history of each iteration.
│   └── iter{1..N}/<UNIT>/ctx/    
│                                 
│
└── iter{1..N}/                   Experiment record. one folder per iteration.
    │                             
    ├── input/                    The frozen inputs for this iteration.
    │   ├── Block{N}.py           The layout at the start of this iteration.
    │   ├── Block{N}.drc.json     The violations found in it.
    │   ├── Block{N}.json         Which parts of the layout must stay electrically
    │   │                         connected — the repair must not break these.
    │   ├── host_leaf.<UNIT>.json The boundary of each single or whole-design unit.
    │   ├── host_union.<UNIT>.json The boundary of each merged unit.
    │   ├── main.md               The knowledge index handed to the agent this time.
    │   ├── knowledge/<LAYER>.md  The layer advice handed to the agent this time — a
    │   │                         snapshot, so you can see exactly what it knew.
    │   ├── skill_official.md     The fixed background instructions, identical every run.
    │   └── knowledge.md          A small pointer file kept for backward compatibility.
    │
    ├── leaves.json               The plan: how the design was split into units.
    ├── unions.json               Which of those units were merged together.
    │
    ├── leaf/                     One folder per repair unit.
    │   └── <UNIT>/
    │       ├── prompt.txt        The exact request sent to the agent.
    │       ├── patch.json        The repair the agent proposed. Missing if it produced
    │       │                     nothing usable.
    │       └── ctx/              The supporting material the agent was given:
    │           ├── crops/        the relevant slices of layout,
    │           ├── drc/          the violations in them,
    │           ├── conn/         the connections that must be preserved,
    │           └── connimpact/   what would break if a connection were cut.
    │
    ├── _gate/                    Scratch space for testing a proposed repair in isolation
    │                             before deciding whether to accept it.
    │
    ├── gated/                    The accept-or-reject decision for each unit.
    │   ├── <UNIT>.verdict        The decision and the measurements behind it.
    │   └── <UNIT>.assembled.json What was actually applied. Absent when the repair was
    │                             rejected.
    │
    ├── score/                    A re-check of units whose repair was only partly
    │   └── <UNIT>.json           applied. Only written when that happens.
    │
    ├── repaired/                 The result of this iteration.
    │   ├── Block{N}.py           The repaired layout — becomes the next iteration's input.
    │   ├── Block{N}.drc.json     The violations remaining in it.
    │   └── _blockeval/           Evidence from the verification step:
    │       ├── Block{N}.gds      the layout in standard chip-design format,
    │       ├── Block{N}.drc.json the violations found,
    │       ├── Block{N}.lyrpt    the checking tool's own report,
    │       ├── Block{N}_render.py the script used to produce them,
    │       └── klayout.log       the tool's log, so the check can be re-run.
    │
    ├── block_result.json         The headline numbers: violations before and after.
    ├── cu_verdicts.json          When two units tried to change the same shared part,
    │                             which one won and why.
    ├── knowledge_update.json     What was learned this iteration. Absent when learning
    │                             is switched off.
    └── ledger_summary.json       An index of this iteration's measurements, linking each
                                  repair back to the layer it affected.
```

## Running EvoDRC

EvoDRC runs as a drop-in replacement for the `agent/` folder of the
[*DAC26 DRC Benchmark*](https://github.com/ASU-VDA-Lab/DAC26_DRC_Benchmark).
You need Docker, a benchmark checkout, and to be logged in to Claude on this
machine (`~/.claude/.credentials.json`, read by the benchmark's own backend).

The benchmark is a git submodule of this repository. Populate it first:

```bash
git submodule update --init DAC26_DRC_Benchmark
```

**1. Build the image**

Two steps, both required. The stock image is missing two
Python packages EvoDRC needs.

```bash
cd ./DAC26_DRC_Benchmark/
docker build -f Dockerfile.repair -t drc-benchmark-repair:latest .
cd ../
docker build -t drc-benchmark-repair:latest - < ./Dockerfile.evodrc
```

The second build only installs two `pip` packages, so it is fed on stdin and needs no build context — that keeps Docker from copying this whole folder, results and all.

**2. Install the agent**

Copy it in; a symlink will not work.

```bash
cd ./DAC26_DRC_Benchmark
mv agent agent_official_backup
cp -r ../agent ./agent
```

**3. Pick a variant** (optional)

Edit `agent/evodrc.conf` and set `ABLATION` to blank for `evodrc`, or to `1`, `2`, or `3` for the ablations described above.

**4. Choose the case and the model.**

Edit the `MODEL_NAMES` and `CASES` arrays in `DAC26_DRC_Benchmark/src/evaluate_claude.sh` to specify the supported models and benchmark cases.

```
MODEL_NAMES=(
  "claude-sonnet-4-6 medium" #Claude Sonnet 4.6 with medium reason effort
  "claude-opus-4-6 high"     #Claude Opus 4.6 with high reason effort
)

CASES=(
  "block|repair|Block1"      #Only supports repair tasks in the DAC'26 benchmark.
  "block|repair|Block2"
  "block|repair|Block3"
  "block|repair|Block4"
  "block|repair|Block5"
  "block|repair|Block6"
  "block|repair|Block7"
)
```

**5. Run**

From the benchmark root. `RECORD_TOKENS=1` is required; without it the run stops immediately.

```bash
cd /path/to/DAC26_DRC_Benchmark
RECORD_TOKENS=1 bash src/evaluate_claude.sh
```

**6. Find the results**

`DAC26_DRC_Benchmark/temp/data/<variant>/Block{N}/<model>/` — for example `temp/data/evodrc/Block5/claude-sonnet-4-6/`.
The variant folder is `evodrc`, `ablation1`, `ablation2` or `ablation3`, matching the `ABLATION` you chose in step 3.

For configuration, authentication and internals, see [`agent/README.md`](agent/README.md).

## Cite this
```
@misc{wu2026evodrcselfevolvingagenticframework,
      title={EvoDRC: A Self-Evolving Agentic Framework for Automated DRC Violation Repair}, 
      author={Bing-Yue Wu and Chia-Tung Ho and Haoyu Yang and Brucek Khailany 
      and Vidya A. Chhabria},
      year={2026},
      eprint={2607.20019},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2607.20019}, 
}
```