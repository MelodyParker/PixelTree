import board
import neopixel
from Effect import Effect
from Effect_Engine import Effect_Engine

PIXEL_PIN = board.D18
NUM_PIXELS = 50
BRIGHTNESS = 1.0

pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False
)


engine = Effect_Engine()


@engine.register_effect_factory("fill-red")
class FillRedEffect(Effect):
    def __init__(self):
        pass
    async def run(self, pixels, *args, **kwargs):
        pixels.fill((0, 255, 0))
        pixels.show()

engine.run_effect("fill-red")