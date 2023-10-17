def novoverse(run):
    def wrapper(*args, **kwargs):
        import sys
        from pathlib import Path

        here = Path(__file__)
        to_append = str(here.resolve().parent.parent.parent)

        sys.path.append(to_append)
        run(*args, **kwargs)

    return wrapper
