<script>
    let apiRoute = $state("red");
    function btnClick() {
        fetch(`http://pi-tree:5000/leds/${apiRoute}`);
    }
</script>

<select name="api-route" id="api-route" bind:value={apiRoute}>
    <option value="red" class="red">Red</option>
    <option value="green" class="green">Green</option>
    <option value="blue" class="blue">Blue</option>
    <option value="off" class="off">Off</option>
</select>
<button onclick={btnClick}>Send command</button>

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