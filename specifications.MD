# API
url: http://pi-tree:5000/

## Routes
### `/api/effects` - GET

fetches the effects available on the server in the following format:

`{"off": {"name": "All Off", "description": "Turns off all LEDs", "params": []}, "fill-red": {"name": "Fill Red", "description": "Colors all LEDs red", "params": []}, "fill-rgb": {"name": "Fill RGB", "description": "Colors all LEDs with the specified RGB color", "params": [{"type": "color", "name": "Color"}]}, "flash-colors": {"name": "Flash Colors", "description": "Flashes all pixels with the given colors", "params": [{"type": "list_N color", "name": "Colors"}, {"type": "list_N number", "name": "Durations"}]}, "alternating-colors": {"name": "Alternate Colors", "description": "Alternates pixels with the given colors", "params": [{"type": "list color", "name": "Colors"}, {"type": "bool", "default": "false", "name": "Move?"}, {"type": "number", "default": "1", "name": "Direction (positive = forward)"}, {"type": "number", "default": "1", "name": "Duration"}]}}`

The types that are supported are 
- `number` - a floating point number
- `color` - an RGB color
- `bool` - a boolean value (true or false)
- `list {typename}` - a list of any length >= 1 of the given type
- `list_{letter} {typename}` - a list of length of the {letter}, is arbitrary, but if there are multiple lists with length_{letter} with the same letter, they must match
- `list_{num} {typename}` - a list of length {num}, Ex: list_5 must have exactly 5 elements

Note that the list parameter can be recursive (list of lists of length 3 would be represented by `list list_3 {typename}`)

### `/effect/run` - POST, OPTIONS (for CORS)

Runs the specified effect

The effect and its parameters are specified with json as in the following example to run the fill-rgb effect:

`{'id': 'fill-rgb', 'rgb': [128, 0, 255]}`


### `/calibrate/<int:pixel>` - GET
Turns off all pixels except for the specified `pixel`, and turns that one white. Used for calibration


### `/leds/red/`- GET
Turns LEDs red

### `/leds/green/` - GET
Turns LEDs green

### `/leds/blue/` - GET
Turns LEDs blue

### `/leds/off/` - GET
Turns LEDs off


# Frontend
You will be developing a Svelte frontend with the following workflow connecting to a pixel control server with the above API specs. General workflow is this:

1. Request all of the effects that can be used.
2. Make a dropdown (or some other input method) of all the effects that exist. Default to the fill-rgb effect if it exists. If it doesn't, just pick the first effect.
3. When the user selects an effect, populate selectors for each of the parameter types. This means you will need to make a separate Svelte component for each of the possible parameter types, populating them with the default values as specified in the earlier API request.
4. Within the effect selection interface, you will have a start effect button (or whatever you want to call it), which will send a POST request to the /api/effect/run endpoint with all of the parameter data. This is pretty straightforward, but an example for the fill-rgb effect is this: 
```js 
async function sendEffect() {
        let id = selectedEffect.id;
        const url = "http://pi-tree:5000/effect/run/";
        const payload = {
            id: id
        };
        if (id == "fill-rgb") {
            let rgb = hexToRgbBitwise(colorSelect);
            payload.rgb = [rgb.r, rgb.g, rgb.b];
        }
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(payload)
            })
            const data = await response.json();
            console.log("We did it!")

        } catch (err) {
            console.error("Error sending data: ", err)
        }
    }
```
5. Once you get back an acknowledgement (a response to the POST request), create a popup in the UI letting the user know that it worked.

Additionally, create a sidebar that keeps track of what effect is running with what parameters.

Your output will be copyable codeblocks for each file you want me to create within an existing Svelte project. Please use Sveltekit conventions for routes (+layout.svelte, +page.svelte, etc), as well as runes for Svelte 5.