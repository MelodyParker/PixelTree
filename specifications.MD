# API
url: http://pi-tree:5000/

## Routes
`/api/effects` - fetches the effects available on the server in the following format:

`{"off": {"name": "All Off", "description": "Turns off all LEDs", "params": []}, "fill-red": {"name": "Fill Red", "description": "Colors all LEDs red", "params": []}, "fill-rgb": {"name": "Fill RGB", "description": "Colors all LEDs with the specified RGB color", "params": [{"type": "color", "name": "Color"}]}, "flash-colors": {"name": "Flash Colors", "description": "Flashes all pixels with the given colors", "params": [{"type": "list color", "length": "N", "name": "Colors"}, {"type": "list number", "length": "N", "name": "Durations"}]}, "alternating-colors": {"name": "Alternate Colors", "description": "Alternates pixels with the given colors", "params": [{"type": "list color", "length": "N", "name": "Colors"}, {"type": "bool", "default": "false", "name": "Move?"}, {"type": "number", "default": "1", "name": "Direction (positive = forward)"}, {"type": "number", "default": "1", "name": "Duration"}]}}`

The types that are supported are 
- number - a floating point number
- color - an RGB color
- bool - a boolean value (true or false)
- 


# Effects
The frontend 