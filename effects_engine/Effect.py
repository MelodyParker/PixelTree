class Effect:
    @staticmethod
    def run(*args, **kwargs):
        raise NotImplementedError("Subclasses need to implement run method")