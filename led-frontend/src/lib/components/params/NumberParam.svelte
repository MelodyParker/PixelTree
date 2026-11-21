<script>
	let { value = 1, onchange, id = '', ariaLabel = 'Number value' } = $props();

	let text = $state(String(value));
	let isFocused = $state(false);

	$effect(() => {
		const incoming = value;
		if (!isFocused) {
			text = String(incoming);
		} else if (
			text !== '' &&
			text !== '-' &&
			text !== '.' &&
			text !== '-.' &&
			Number(text) !== incoming
		) {
			text = String(incoming);
		}
	});

	function handleInput(event) {
		const raw = event.currentTarget.value;
		text = raw;
		if (raw.trim() === '' || raw === '-' || raw === '.' || raw === '-.') return;
		const parsed = Number(raw);
		if (Number.isFinite(parsed)) {
			onchange(parsed);
		}
	}

	function handleBlur() {
		isFocused = false;
		const parsed = Number(text);
		if (text.trim() === '' || !Number.isFinite(parsed)) {
			text = String(value);
		} else {
			text = String(parsed);
			onchange(parsed);
		}
	}

	function step(delta) {
		const next = Number((Number(value || 0) + delta).toFixed(4));
		text = String(next);
		onchange(next);
	}
</script>

<div class="number-param">
	<button
		type="button"
		class="btn btn-icon step-btn"
		onclick={() => step(-1)}
		aria-label="Decrease by 1"
		title="Decrease by 1"
	>
		−
	</button>
	<input
		{id}
		type="text"
		inputmode="decimal"
		class="input mono num-input"
		value={text}
		aria-label={ariaLabel}
		onfocus={() => (isFocused = true)}
		oninput={handleInput}
		onblur={handleBlur}
	/>
	<button
		type="button"
		class="btn btn-icon step-btn"
		onclick={() => step(1)}
		aria-label="Increase by 1"
		title="Increase by 1"
	>
		+
	</button>
</div>

<style>
	.number-param {
		display: inline-flex;
		align-items: center;
		gap: var(--space-xs);
		width: 100%;
		max-width: 240px;
	}

	.num-input {
		text-align: center;
	}

	.step-btn {
		flex-shrink: 0;
		font-weight: 700;
	}
</style>