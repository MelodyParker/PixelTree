<script>
	let { value = false, onchange, id = '', ariaLabel = 'Boolean toggle' } = $props();

	function toggle() {
		onchange(!value);
	}
</script>

<div class="bool-param">
	<button
		{id}
		type="button"
		role="switch"
		aria-checked={Boolean(value)}
		aria-label={ariaLabel}
		class="switch"
		class:checked={Boolean(value)}
		onclick={toggle}
	>
		<span class="thumb"></span>
	</button>
	<span class="state-label mono" class:active={Boolean(value)}>
		{value ? 'true' : 'false'}
	</span>
</div>

<style>
	.bool-param {
		display: inline-flex;
		align-items: center;
		gap: var(--space-sm);
		min-height: var(--control-height);
	}

	.switch {
		position: relative;
		width: 46px;
		height: 26px;
		padding: 0;
		border-radius: 999px;
		border: 1px solid var(--border-strong);
		background: var(--surface-subtle);
		transition:
			background-color 0.16s ease,
			border-color 0.16s ease;
	}

	.switch.checked {
		background: var(--accent);
		border-color: var(--accent);
	}

	.thumb {
		position: absolute;
		top: 2px;
		left: 2px;
		width: 20px;
		height: 20px;
		border-radius: 50%;
		background: #ffffff;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
		transition: transform 0.16s ease;
	}

	.switch.checked .thumb {
		transform: translateX(20px);
	}

	.state-label {
		font-size: 0.9em;
		color: var(--text-muted);
	}

	.state-label.active {
		color: var(--text);
		font-weight: 600;
	}
</style>