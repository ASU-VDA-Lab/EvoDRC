# EvoDRC
This repository contains the experimental data from the EvoDRC paper and the executable EvoDRC framework for iteratively refining skill files during the agentic DRC repair of VLSI circuit layouts.

## Framework Description
![Inference](etc/EvoDRC.png)
Design rule check (DRC) closure remains a major bottleneck in advanced-node physical design. Although detailed routers are rule-aware, residual design rule violations (DRVs) often require manual engineering change order iterations. Automating this process is challenging because repairs must account for complex geometric interactions, preserve circuit connectivity, and avoid introducing new violations.
We present EvoDRC, a skill-evolution framework for agentic block-level DRC repair. EvoDRC initializes layer-specific repair skills using knowledge distilled from an unrelated reference design and continuously evolves these skills using traceable repair experience collected from the target design. EvoDRC decomposes the layout into bounded repair regions and assigns an LLM repair agent to each region. Local DRC analysis, connectivity-checking, and impact-preview tools provide feedback on proposed modifications. Repair operations and their resulting DRV changes are stored in a knowledge database and used to evolve the repair skills. Experiments on seven block-level designs from the DAC26 DRC Benchmark show that EvoDRC achieves a 73.5\% overall reduction compared to the reported baseline. 

## EvoDRC structure

```
agent/                 EvoDRC agentic framework, replace the agent/ in DAC26_DRC_Benchmark with this

data/                  Experimental data in the paper
└── <EXP>/             EvoDRC or ablation studies
    └── Block{N}/      one chip design (Block1 … Block7)
        └── <Model>/   the AI model used (claude-sonnet-4-6 with Claude Code)

cla_gds/               the external design with/without DRC      
├──carry_lookahead_adder_clean.gds
└──carry_lookahead_adder.gds           
```

### The four variants (`<EXP>`)

| Folder | What is different |
|---|---|
| `evodrc` | The main method. Starts with prior experience and keeps learning. |
| `ablation1` | Starts with the rules but **no prior experience** — learns from scratch. |
| `ablation2` | Starts with experience but **stops learning** since the first iteration. |
| `ablation3` | Repairs the design **as a whole** instead of splitting it into pieces. |

Comparing these four shows how much the prior experience and the continued learning
actually contribute.

### Names you will see in the data/ tree

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

## Cite this
```
@misc{wu2026evodrcselfevolvingagenticframework,
      title={EvoDRC: A Self-Evolving Agentic Framework for Automated DRC Violation Repair}, 
      author={Bing-Yue Wu and Chia-Tung Ho and Haoyu Yang and Brucek Khailany and Vidya A. Chhabria},
      year={2026},
      eprint={2607.20019},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2607.20019}, 
}
```