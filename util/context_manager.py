import traceback


class ContextManager:
    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        del self
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True
