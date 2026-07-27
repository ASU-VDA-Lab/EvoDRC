# EvoDRC agent package marker.
#
# This package is dropped into ``DAC26_DRC_Benchmark/agent/`` and invoked by
# the frozen benchmark pipeline. The dispatcher lives in ``agent/agent.py``;
# back-end adapters in the benchmark's consolidated ``src/agent_backend/``
# package; EvoDRC pipeline in ``agent/src/``. See
# ``codebase_design/advisor/combine.md`` for the canonical architecture
# (Phase 6 implementer output).
