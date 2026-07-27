"""EvoDRC: block-level DRC repair sub-package.

Top-level re-exports kept minimal so that `agent/agent.py` can keep
importing `agent.src.tokens` without forcing the rest of the pipeline
to load.
"""


__all__ = ["run_pipeline", "run_src_block_repair"]


def run_pipeline(ctx):  # pragma: no cover - thin re-export
    from .pipeline import run_pipeline as _impl
    return _impl(ctx)


def run_src_block_repair(prompt_path, output_path, temp_dir,
                                workspace, model_name):  # pragma: no cover
    from .agent_entry import run_src_block_repair as _impl
    return _impl(prompt_path, output_path, temp_dir, workspace, model_name)
