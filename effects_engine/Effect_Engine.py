import asyncio
from Effect import Effect
from typing import Optional, Dict

class Effect_Engine:
    def __init__(self, pixels):
        self.registered_effects: Dict[str, type[Effect]] = {}
        self.pixels = pixels
        self.active_task: Optional[asyncio.Task] = None

    def register_effect(self, cls, name):
        if issubclass(cls, Effect):
            self.registered_effects[name] = cls
    
    def register_effect_factory(self, name):
        def decorator(cls):
            self.register_effect(cls, name)
            return cls
        return decorator
    
    async def run_effect(self, name, *args, **kwargs):
        effect = self.registered_effects.get(name)
        if effect is None:
            raise KeyError("Unregistered effect")
        if self.active_task and not self.active_task.done():
            print("Cancelling ongoing effect")
            self.active_task.cancel()
            try:
                await self.active_task
            except asyncio.CancelledError:
                print("Old effect killed successfully")
        self.active_task = asyncio.create_task(effect.run(self.pixels, *args, **kwargs))
        
    
