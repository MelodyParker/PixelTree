<script>
	import {
		COLOR_PRESETS,
		clampByte,
		hexToRgb,
		normalizeRgb,
		rgbToHex
	} from '$lib/utils/color.js';

	let { value = [255, 255, 255], onchange, id = '', ariaLabel = 'RGB color' } = $props();

	let rgb = $derived(normalizeRgb(value));
	let hex = $derived(rgbToHex(rgb));

	let hexDraft = $state(rgbToHex(normalizeRgb(value)));
	let hexFocused = $state(false);

	$effect(() => {
		const currentHex = hex;
		if (!hexFocused) {
			hexDraft = currentHex;
		}
	});

	function handlePickerInput(event) {
		const parsed = hexToRgb(event.currentTarget.value);
		if (parsed) {
			hexDraft = rgbToHex(parsed);
			onchange(parsed);
		}
	}

	function handleHexInput(event) {
		const raw = event.currentTarget.value;
		hexDraft = raw;
		const parsed = hexToRgb(raw);
		if (parsed) {
			onchange(parsed);
		}
	}

	function handleHexBlur() {
		hexFocused = false;
		hexDraft = hex;
	}

	function handleChannel(index, event) {
		const next = [...rgb];
		next[index] = clampByte(event.currentTarget.value);
		onchange(next);
	}
</script>

<div class="color-param">
	<div class="primary-row">
		<label class="swatch-wrap" title="Pick color">
			<input
				{id}
				type="color"
				class="native-picker"
				value={hex}
				aria-label={ariaLabel}
				oninput={handlePickerInput}
			/>
			<span class="swatch-visual" style:background={hex}></span>
		</label>

		<input
			type="text"
			class="input mono hex-input"
			value={hexDraft}
			maxlength="7"
			aria-label="Hex color"
			onfocus={() => (hexFocused = true)}
			oninput={handleHexInput}
			onblur={handleHexBlur}
		/>

		<div class="rgb-channels">
			<label class="channel">
				<span class="ch-tag r">R</span>
				<input
					type="number"
					min="0"
					max="255"
					class="input mono ch-input"
					value={rgb[0]}
					oninput={(e) => handleChannel(0, e)}
				/>
			</label>
			<label class="channel">
				<span class="ch-tag g">G</span>
				<input
					type="number"
					min="0"
					max="255"
					class="input mono ch-input"
					value={rgb[1]}
					oninput={(e) => handleChannel(1, e)}
				/>
			</label>
			<label class="channel">
				<span class="ch-tag b">B</span>
				<input
					type="number"
					min="0"
					max="255"
					class="input mono ch-input"
					value={rgb[2]}
					oninput={(e) => handleChannel(2, e)}
				/>
			</label>
		</div>
	</div>

	<div class="presets">
		{#each COLOR_PRESETS as preset}
			<button
				type="button"
				class="preset-dot"
				class:selected={rgbToHex(preset.rgb) === hex}
				style:background={rgbToHex(preset.rgb)}
				title={`${preset.name} [${preset.rgb.join(', ')}]`}
				aria-label={`Set color to ${preset.name}`}
				onclick={() => onchange([...preset.rgb])}
			></button>
		{/each}
	</div>
</div>

<style>
	.color-param {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
		width: 100%;
	}

	.primary-row {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: var(--space-xs);
	}

	.swatch-wrap {
		position: relative;
		width: var(--control-height);
		height: var(--control-height);
		flex-shrink: 0;
		cursor: pointer;
	}

	.native-picker {
		position: absolute;
		inset: 0;
		width: 100%;
		height: 100%;
		opacity: 0;
		cursor: pointer;
	}

	.swatch-visual {
		display: block;
		width: 100%;
		height: 100%;
		border-radius: var(--radius-sm);
		border: 2px solid var(--border-strong);
		box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.2);
	}

	.hex-input {
		width: 96px;
		text-transform: uppercase;
	}

	.rgb-channels {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 6px;
	}

	.channel {
		display: inline-flex;
		align-items: center;
		gap: 4px;
	}

	.ch-tag {
		font-size: 0.78em;
		font-weight: 700;
		width: 14px;
		text-align: center;
	}

	.ch-tag.r {
		color: #f87171;
	}
	.ch-tag.g {
		color: #4ade80;
	}
	.ch-tag.b {
		color: #60a5fa;
	}

	.ch-input {
		width: 66px;
		padding: 0 6px;
		text-align: center;
	}

	.presets {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		align-items: center;
	}

	.preset-dot {
		width: 20px;
		height: 20px;
		padding: 0;
		border-radius: 50%;
		border: 2px solid var(--border);
		transition: transform 0.1s ease, border-color 0.1s ease;
	}

	.preset-dot:hover {
		transform: scale(1.15);
		border-color: var(--text);
	}

	.preset-dot.selected {
		border-color: var(--accent);
		box-shadow: 0 0 0 2px var(--accent-soft);
	}
</style>