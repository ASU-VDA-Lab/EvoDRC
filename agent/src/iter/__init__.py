"""Version B iterative block-repair controller package.

All modules here run ENTIRELY inside ONE DAC26 repair container during the
agent phase. They reuse the run7 ``src`` decompose stages + per-leaf
prompt builder + connectivity / DRC helpers, and drive an iterative
decompose -> repair-every-leaf -> connectivity-gate -> assemble -> block-DRC
-> knowledge -> re-decompose loop. No module here imports the DAC26
``/workspace/evaluator`` scorer bundle (absent during the agent phase); the
connectivity gate uses the bind-mounted ``evaluator_helpers/check_connectivity``
and the DRC uses the vendored ``drc_postprocess`` + KLayout. All prose is
English; PYTHONHASHSEED=0 keeps decomposition deterministic.
"""
