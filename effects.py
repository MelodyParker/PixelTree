import board
import neopixel
import asyncio
from effects_engine.Effect import Effect
from effects_engine.Effects_Engine import Effects_Engine
import math

PIXEL_PIN = board.D18
NUM_PIXELS = 50
BRIGHTNESS = 1.0

def gamma_correct(color):
    # A standard gamma value for NeoPixels
    gamma_val = 3
    
    # Unpack RGB tuple
    r, g, b = color
    
    # Apply the gamma curve to each channel
    # Normalizing by 255.0, raising to power of gamma, then multiplying by 255
    r_corr = int(pow(r / 255.0, gamma_val) * 255.0)
    g_corr = int(pow(g / 255.0, gamma_val) * 255.0)
    b_corr = int(pow(b / 255.0, gamma_val) * 255.0)
    
    return (r_corr, g_corr, b_corr)

def lerp(low, high, prop):
    return low + (high - low) * prop 


pixels = neopixel.NeoPixel(
    PIXEL_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.RGB
)


engine = Effects_Engine(pixels)
odd_engine = Effects_Engine(pixels[::2])
even_engine = Effects_Engine(pixels[1::2])


@engine.register_effect_factory("off", name="All Off", description="Turns off all LEDs", params=[])
class OffEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((0, 0, 0))
        pixels.show()

@engine.register_effect_factory("fill-red", name="Fill Red", description="Colors all LEDs red", params=[])
class FillRedEffect(Effect):
    @staticmethod
    async def run(pixels, *args, **kwargs):
        pixels.fill((255, 0, 0))
        pixels.show()

@engine.register_effect_factory("fill-rgb", name="Fill RGB", 
                                description="Colors all LEDs with the specified RGB color",
                                params=[{"type": "color", "name": "Color"}])
class FillRGBEffect(Effect):
    @staticmethod
    async def run(pixels, rgb, *args, **kwargs):
        # r, g, b = rgb
        pixels.fill(gamma_correct(rgb))
        pixels.show()

@engine.register_effect_factory("flash-colors", name="Flash Colors",
                                description="Flashes all pixels with the given colors",
                                params=[{"type": "list color", "length": "N", "name": "Colors"}, 
                                        {"type": "list number", "length": "N", "name": "Durations"}])
class FlashColorsEffect(Effect):
    @staticmethod
    async def run(pixels, colors, durations, *args, **kwargs):
        while True:
            for color, duration in zip(colors, durations):
                # r, g, b = color
                pixels.fill(color)
                pixels.show()
                await asyncio.sleep(duration)

@engine.register_effect_factory("alternating-colors", name="Alternate Colors",
                                description="Alternates pixels with the given colors",
                                params=[{"type": "list color", "length": "N", "name": "Colors"},
                                        {"type": "bool", "default": "false", "name": "Move?"},
                                        {"type": "number", "default": "1", "name": "Direction (positive = forward)"},
                                        {"type": "number", "default": "1", "name": "Duration"}])
class AlternatingColorsEffect(Effect):
    @staticmethod
    # direction 1 means forwards, direction -1 means backwards
    async def run(pixels, colors, move=False, direction=1, duration=1, *args, **kwargs):
        num_colors = len(colors)
        if not move:
            for i, pixel in enumerate(pixels):
                color = colors[i % num_colors]
                pixels[i] = gamma_correct(color)
            pixels.show()
            return
        offset = 0
        while True:
            for i, pixel in enumerate(pixels):
                color = colors[(i + offset) % num_colors]
                pixels[i] = gamma_correct(color)
            pixels.show()
            offset -= direction
            await asyncio.sleep(duration)

@engine.register_effect_factory("gradient", name="Gradient", description="Gradient between given colors", params=[
    {"type": "list color", "length": "N", "name": "Colors"}
])
class GradientEffect(Effect):
    @staticmethod
    async def run(pixels, colors, move=False, direction=1, duration=1):
        num_colors = len(colors)
        num_pixels = len(pixels)
        if not move:
            for i, pixel in enumerate(pixels):
                num = (i / num_pixels) * (num_colors - 1)
                color_1 = math.floor(num)
                color_2 = math.ceil(num)
                frac = num - color_1
                r1, g1, b1 = colors[color_1]
                r2, g2, b2 = colors[color_2]
                rg = lerp(r1, r2, frac)
                gg = lerp(g1, g2, frac)
                bg = lerp(b1, b2, frac)
                pixels[i] = gamma_correct((rg, gg, bg))
            pixels.show()

                





async def main():
    try:
        while True:
            # await engine.run_effect("alternating-colors", [(228, 3, 3), (255, 140, 0), (255, 237, 0), (0, 128, 38), (0, 76, 255), (115, 41, 130)], True, 2, 1)
            # await engine.run_effect("fill-rgb", rgb=(255, 255, 255), pixels=pixels[::2])
            await engine.run_effect("gradient", colors=[(255, 255, 0), (255, 255, 0), (255, 0, 255), (255, 0, 255), (255, 255, 0), (255, 255, 0)])
            await asyncio.sleep(float('inf'))
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