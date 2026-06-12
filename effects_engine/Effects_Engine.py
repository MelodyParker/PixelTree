import asyncio
from effects_engine.Effect import Effect
from typing import Optional, Dict
from json import dumps

class Effects_Engine:
    def __init__(self, pixels):
        self.registered_effects: Dict[str, type[Effect]] = {}
        self.effects_info = {}
        self.pixels = pixels
        self.active_task: Optional[asyncio.Task] = None

    def register_effect(self, cls, id, name, description, params):
        if issubclass(cls, Effect):
            self.registered_effects[id] = cls
            effect_info = {
                "name": name,
                "description": description,
                "params": params
            }
            self.effects_info[id] = effect_info
    
    def register_effect_factory(self, id, name, description, params):
        def decorator(cls):
            self.register_effect(cls, id, name, description, params)
            return cls
        return decorator
    
    def effects_to_json(self):
        return dumps(self.effects_info)
    
    async def run_effect(self, name, pixels=None, *args, **kwargs):
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
        self.active_task = asyncio.create_task(effect.run((pixels if pixels is not None else self.pixels), *args, **kwargs))
        
    
