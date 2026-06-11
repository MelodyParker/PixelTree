<script>
    import BoolInput from "./BoolInput.svelte";
import ColorInput from "./ColorInput.svelte";
    import NumberInput from "./NumberInput.svelte";
    let { length = $bindable(1), value = $bindable(new Array(length)), type, name } = $props();
</script>

{#each 1..length as i (i)}
    {#if type == "number"}
        <NumberInput bind:value={value[i]} name={`${name} ${i + 1}`} />
    {:else if type == "color"}
        <ColorInput bind:value={value[i]} name={`${name} ${i + 1}`} />
    {:else if type == "bool"}
        <BoolInput bind:value={value[i]} name={`${name} ${i + 1}`} />
    {:else}
        Invalid type {type}.
    {/if}
{/each}