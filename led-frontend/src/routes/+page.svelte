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
    function btnClick() {
        fetch(`http://pi-tree:5000/leds/${apiRoute}`);
    }

    let selectedEffect = $state({id: "", params: []});
</script>

{#if loadPage}
{effectsData.data}


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

<!-- <select name="hi" id="hi">
    {#each [1, 2, 3] as i} 
        <option>{i}</option>
    {/each}
</select> -->

<select name="api-route" id="api-route" bind:value={apiRoute}>
    <option value="red" class="red">Red</option>
    <option value="green" class="green">Green</option>
    <option value="blue" class="blue">Blue</option>
    <option value="off" class="off">Off</option>
</select>
<button onclick={btnClick}>Send command</button>
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