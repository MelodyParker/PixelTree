<script>
    let { value = $bindable("#ffffff"), name} = $props();
</script>

<label for="color-input">{name}:</label>
<input type="color" name="input-color" id="color-input" bind:value={value}>