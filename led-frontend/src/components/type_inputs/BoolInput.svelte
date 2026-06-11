<script>
    let { value = $bindable(false), name } = $props();
</script>

<label for="bool-input"></label>
<input type="checkbox" name="bool-input" id="bool-input" bind:value={value}>