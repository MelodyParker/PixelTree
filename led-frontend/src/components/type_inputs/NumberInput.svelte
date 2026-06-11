<script>
    let { value = $bindable(1), name } = $props();
</script>

<label for="number-input">{name}:</label>
<input type="number" name="number-input" id="number-input" bind:value={value}>