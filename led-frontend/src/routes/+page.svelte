<script>
    import { onMount } from "svelte";
    import { effectsData } from "$lib/stores.svelte";
    import NumberInput from "../components/type_inputs/NumberInput.svelte";
    import ColorInput from "../components/type_inputs/ColorInput.svelte";
    import BoolInput from "../components/type_inputs/BoolInput.svelte";

    let loadPage = $state(false);
    onMount(async () => {
        let response = await fetch("http://pi-tree:5000/api/effects");
        response.json().then(json => {
            effectsData.data = json;
            console.log(json)
            loadPage = true;
        })
    })

    let apiRoute = $state("red");
    async function sendEffect() {
        let id = selectedEffect.id;
        const url = "http://pi-tree:5000/effect/run/";
        const payload = {
            id: id
        };
        if (id == "fill-rgb") {
            payload.rgb = [rgb_r, rgb_g, rgb_b];
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

    let selectedEffect = $state({id: "", params: []});
    let rgb_r = $state(0);
    let rgb_g = $state(0);
    let rgb_b = $state(0);
</script>

{#if loadPage}
{effectsData.data}
<form onsubmit={sendEffect}>

<select name="effect-selector" id="effect-selector" bind:value={selectedEffect.id}>
    {#each Object.entries(effectsData.data) as [effect_id, effect], i}
        <option value={effect_id}>{effect.name}</option>
        <!-- {#each effect.params as param, j (param.name)}
            {#if param.type == "number"}
            <NumberInput bind:value={selectedEffect.params[j]} name={param.name} />
            {:else if param.type == "color"}
            <ColorInput bind:value={selectedEffect.params[j]} name={param.name} />
            {:else if param.type == "bool"}
            <BoolInput bind:value={selectedEffect.params[j]} name={param.name} />
            {:else}
            Invalid type {param.type}
            {/if}
        {/each} -->
    {/each}
</select>

<input type="number" min="0" max="255" bind:value={rgb_r}>
<input type="number" min="0" max="255" bind:value={rgb_g}>
<input type="number" min="0" max="255" bind:value={rgb_b}>

<!-- <select name="hi" id="hi">
    {#each [1, 2, 3] as i} 
        <option>{i}</option>
    {/each}
</select> -->
<button type="submit" onclick={sendEffect}>Start Effect</button>
</form>
{/if}


<style>
    .red {
        background-color: red;
    }
    .green {
        background-color: green;
    }
    .blue {
        background-color: blue;
    }
    .off {
        background-color: grey;
    }
    option:hover {
        background-color: blue;
    }
</style>