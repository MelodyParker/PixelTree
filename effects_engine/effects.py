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

@engine.register_effect_factory("off")
class OffEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((0, 0, 0))
        pixels.show()

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

@engine.register_effect_factory("alternating-colors")
class AlternatingColorsEffect(Effect):
    @staticmethod
    async def run(pixels, colors, move=False, *args, **kwargs):
        num_colors = len(colors)
        if not move:
            for i, pixel in enumerate(pixels):
                r, g, b = colors[i % num_colors]
                pixels[i] = (g, r, b)
            pixels.show()



async def main():
    try:
        while True:
            await engine.run_effect("alternating-colors", [(255, 0, 0), (0, 255, 0)])
            await asyncio.sleep(10)
            # await engine.run_effect("flash-colors", [(255, 0, 0), (0, 255, 0), (0, 0, 255)], [0.3, 0.3, 0.4]) # make it green?
            # await asyncio.sleep(3)
            # await engine.run_effect("off")
            # await asyncio.sleep(0.3)
            # await engine.run_effect("fill-rgb", (255, 255, 0))
            # await asyncio.sleep(1)
            # await engine.run_effect("off")
            # await asyncio.sleep(0.3)
            # await engine.run_effect("flash-colors", [(255, 255, 0), (0, 255, 255), (255, 0, 255)], [1, 1, 1])
            # await asyncio.sleep(4)
            # await engine.run_effect("off")
            # await asyncio.sleep(0.3)
    finally:
        await engine.run_effect("off")

asyncio.run(main())