import asyncio
from Effect import Effect

class Effect_Engine:
    def __init__(self, pixels):
        self.registered_effects = {}
        self.pixels = pixels
    def register_effect(self, cls, name):
        if issubclass(cls, Effect):
            self.registered_effects[name] = cls
    
    def register_effect_factory(self, name):
        def decorator(cls):
            self.register_effect(cls, name)
            return cls
        return decorator
    
    async def run_effect(self, name):
        if not self.registered_effects.get(name):
            raise KeyError("Unregistered effect")
        effect = self.registered_effects.get(name)
        asyncio.run(await effect.run())
        
    
