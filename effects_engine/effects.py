import board
import neopixel
import asyncio
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


engine = Effect_Engine(pixels)


@engine.register_effect_factory("fill-red")
class FillRedEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((0, 255, 0))
        pixels.show()

@engine.register_effect_factory("fill-rgb")
class FillRGBEffect(Effect):
    @staticmethod
    async def run(pixels, rgb, *args, **kwargs):
        r, g, b = rgb
        pixels.fill((g, r, b))
        pixels.show()

@engine.register_effect_factory("flash-colors")
class FlashColors(Effect):
    @staticmethod
    async def run(pixels, colors, durations, *args, **kwargs):
        while True:
            for color, duration in zip(colors, durations):
                r, g, b = color
                pixels.fill((g, r, b))
                pixels.show()
                await asyncio.sleep(duration)

async def main():
    while True:
        await engine.run_effect("flash-colors", [(255, 0, 0), (0, 255, 0), (0, 0, 255)], [0.3, 0.3, 0.4]) # make it green?
        await asyncio.sleep(3)
        await engine.run_effect("fill-rgb", (0, 0, 0))
        await asyncio.sleep(1)

asyncio.run(main())