import board
import neopixel
import asyncio
from Effect import Effect
from Effect_Engine import Effect_Engine


PIXEL_PIN = board.D18
NUM_PIXELS = 50
BRIGHTNESS = 1.0

def gamma_correct(color):
    # A standard gamma value for NeoPixels
    gamma_val = 2.7
    
    # Unpack RGB tuple
    r, g, b = color
    
    # Apply the gamma curve to each channel
    # Normalizing by 255.0, raising to power of gamma, then multiplying by 255
    r_corr = int(pow(r / 255.0, gamma_val) * 255.0)
    g_corr = int(pow(g / 255.0, gamma_val) * 255.0)
    b_corr = int(pow(b / 255.0, gamma_val) * 255.0)
    
    return (r_corr, g_corr, b_corr)



pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
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
        # r, g, b = rgb
        pixels.fill(rgb)
        pixels.show()

@engine.register_effect_factory("flash-colors")
class FlashColors(Effect):
    @staticmethod
    async def run(pixels, colors, durations, *args, **kwargs):
        while True:
            for color, duration in zip(colors, durations):
                # r, g, b = color
                pixels.fill(color)
                pixels.show()
                await asyncio.sleep(duration)

@engine.register_effect_factory("alternating-colors")
class AlternatingColorsEffect(Effect):
    @staticmethod
    async def run(pixels, colors, move=False, *args, **kwargs):
        num_colors = len(colors)
        if not move:
            for i, pixel in enumerate(pixels):
                color = colors[i % num_colors]
                pixels[i] = color
            pixels.show()



async def main():
    try:
        while True:
            await engine.run_effect("alternating-colors", [gamma_correct((91, 206, 205)), gamma_correct((245, 169, 184)), gamma_correct((255, 255, 255))])
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