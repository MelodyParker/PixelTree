<script>
	import { testConnection } from '$lib/api/client.js';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { historyStore } from '$lib/stores/history.svelte.js';
	import { ACCENT_PRESETS, settings } from '$lib/stores/settings.svelte.js';
	import { toasts } from '$lib/stores/toasts.svelte.js';

	let urlDraft = $state(settings.apiBaseUrl);
	let testing = $state(false);
	let connectionStatus = $state(null);

	function handleSaveUrl() {
		if (!urlDraft.trim()) {
			toasts.error('Invalid URL', 'Please enter a valid API base URL.');
			return;
		}
		settings.setApiBaseUrl(urlDraft);
		urlDraft = settings.apiBaseUrl;
		effectsStore.load(true);
		toasts.success('API URL Saved', `Now targeting ${settings.apiBaseUrl}`);
	}

	async function handleTestConnection() {
		testing = true;
		connectionStatus = null;
		try {
			const result = await testConnection(urlDraft);
			connectionStatus = {
				ok: true,
				text: `Connected (${result.count} effects found in ${result.latencyMs} ms)`
			};
		} catch (err) {
			connectionStatus = {
				ok: false,
				text: err.message
			};
		} finally {
			testing = false;
		}
	}

	function handleHistoryLimitChange(event) {
		const val = Number(event.currentTarget.value);
		settings.setHistoryLimit(val);
		historyStore.trimToLimit(settings.historyLimit);
	}

	function handleResetSettings() {
		settings.reset();
		urlDraft = settings.apiBaseUrl;
		connectionStatus = null;
		toasts.info('Settings Reset', 'Restored all appearance and server defaults.');
	}

	function handleClearHistory() {
		historyStore.clearAll();
		toasts.info('History Cleared', 'Cleared active state and recent effect history.');
	}
</script>

<svelte:head>
	<title>Settings · Pi-Tree Controller</title>
</svelte:head>

<div class="settings-page">
	<div class="page-head">
		<h1>Settings</h1>
		<p class="muted">
			Customize the interface and server connection. All preferences are stored automatically in your browser.
		</p>
	</div>

	<div class="settings-grid">
		<!-- Appearance -->
		<section class="card panel">
			<h2>Appearance</h2>

			<div class="setting-row">
				<div class="setting-info">
					<span class="setting-label">Theme</span>
					<span class="muted small">Switch between dark and light surfaces.</span>
				</div>
				<div class="segmented">
					<button
						type="button"
						class="seg-btn"
						class:active={settings.theme === 'dark'}
						onclick={() => settings.setTheme('dark')}
					>
						☾ Dark
					</button>
					<button
						type="button"
						class="seg-btn"
						class:active={settings.theme === 'light'}
						onclick={() => settings.setTheme('light')}
					>
						☀ Light
					</button>
				</div>
			</div>

			<div class="setting-row column">
				<div class="setting-info">
					<span class="setting-label">Primary Accent Color</span>
					<span class="muted small">Applies to primary actions, active tabs, and focus rings.</span>
				</div>

				<div class="accent-controls">
					<label class="color-picker-pill">
						<input
							type="color"
							value={settings.accentColor}
							oninput={(e) => settings.setAccentColor(e.currentTarget.value)}
						/>
						<span class="mono">{settings.accentColor}</span>
					</label>

					<div class="preset-swatches">
						{#each ACCENT_PRESETS as preset}
							<button
								type="button"
								class="swatch-btn"
								class:selected={settings.accentColor.toLowerCase() === preset.hex.toLowerCase()}
								style:background={preset.hex}
								title={preset.name}
								aria-label={`Use ${preset.name} accent color`}
								onclick={() => settings.setAccentColor(preset.hex)}
							></button>
						{/each}
					</div>
				</div>
			</div>

			<div class="setting-row">
				<div class="setting-info">
					<span class="setting-label">Corner Radius</span>
					<span class="muted small">Adjust roundness of cards, inputs, and buttons.</span>
				</div>
				<div class="segmented">
					{#each ['sharp', 'balanced', 'rounded'] as radius}
						<button
							type="button"
							class="seg-btn cap"
							class:active={settings.borderRadius === radius}
							onclick={() => settings.setBorderRadius(radius)}
						>
							{radius}
						</button>
					{/each}
				</div>
			</div>

			<div class="setting-row">
				<div class="setting-info">
					<span class="setting-label">UI Density</span>
					<span class="muted small">Control spacing and input sizing.</span>
				</div>
				<div class="segmented">
					{#each ['compact', 'comfortable', 'spacious'] as density}
						<button
							type="button"
							class="seg-btn cap"
							class:active={settings.density === density}
							onclick={() => settings.setDensity(density)}
						>
							{density}
						</button>
					{/each}
				</div>
			</div>
		</section>

		<!-- Server & Data -->
		<section class="card panel">
			<h2>Server &amp; History</h2>

			<div class="setting-row column">
				<label for="api-url-input" class="setting-info">
					<span class="setting-label">API Base URL</span>
					<span class="muted small">Base address of your Pi pixel control server (no trailing slash).</span>
				</label>
				<div class="url-row">
					<input
						id="api-url-input"
						type="url"
						class="input mono"
						bind:value={urlDraft}
						placeholder="http://pi-tree:5000"
					/>
					<button type="button" class="btn btn-primary" onclick={handleSaveUrl}>
						Save
					</button>
					<button
						type="button"
						class="btn"
						disabled={testing}
						onclick={handleTestConnection}
					>
						{testing ? 'Testing…' : 'Test'}
					</button>
				</div>

				{#if connectionStatus}
					<div
						class="test-result"
						class:ok={connectionStatus.ok}
						class:err={!connectionStatus.ok}
					>
						{connectionStatus.text}
					</div>
				{/if}
			</div>

			<div class="setting-row">
				<label for="history-limit" class="setting-info">
					<span class="setting-label">History Limit</span>
					<span class="muted small">Maximum number of recent runs kept in the sidebar (1–100).</span>
				</label>
				<input
					id="history-limit"
					type="number"
					min="1"
					max="100"
					class="input mono limit-input"
					value={settings.historyLimit}
					onchange={handleHistoryLimitChange}
				/>
			</div>

			<div class="divider"></div>

			<div class="setting-row">
				<div class="setting-info">
					<span class="setting-label">Clear Saved History</span>
					<span class="muted small">
						Removes the active effect readout and all {historyStore.entries.length} stored runs.
					</span>
				</div>
				<button type="button" class="btn btn-danger btn-sm" onclick={handleClearHistory}>
					Clear History
				</button>
			</div>

			<div class="setting-row">
				<div class="setting-info">
					<span class="setting-label">Reset All Settings</span>
					<span class="muted small">Restore default theme, accent color, layout, and API URL.</span>
				</div>
				<button type="button" class="btn btn-sm" onclick={handleResetSettings}>
					Reset Defaults
				</button>
			</div>
		</section>
	</div>
</div>

<style>
	.settings-page {
		display: flex;
		flex-direction: column;
		gap: var(--space-lg);
	}

	.page-head {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	h1 {
		font-size: 1.5em;
		letter-spacing: -0.02em;
	}

	h2 {
		font-size: 1.15em;
		padding-bottom: var(--space-xs);
		border-bottom: 1px solid var(--border);
	}

	.settings-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
		gap: var(--space-lg);
		align-items: start;
	}

	.panel {
		padding: var(--space-lg);
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.setting-row {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	.setting-row.column {
		flex-direction: column;
		align-items: stretch;
		gap: var(--space-sm);
	}

	.setting-info {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.setting-label {
		font-weight: 600;
	}

	.small {
		font-size: 0.85em;
	}

	.segmented {
		display: inline-flex;
		padding: 3px;
		border-radius: var(--radius-sm);
		background: var(--surface-subtle);
		border: 1px solid var(--border);
		gap: 3px;
	}

	.seg-btn {
		padding: 6px 12px;
		border: none;
		border-radius: calc(var(--radius-sm) - 2px);
		background: transparent;
		color: var(--text-muted);
		font-weight: 500;
		font-size: 0.9em;
	}

	.seg-btn:hover {
		color: var(--text);
	}

	.seg-btn.active {
		background: var(--accent);
		color: var(--accent-contrast);
		font-weight: 600;
	}

	.cap {
		text-transform: capitalize;
	}

	.accent-controls {
		display: flex;
		align-items: center;
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	.color-picker-pill {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		padding: 4px 10px 4px 6px;
		border-radius: var(--radius-sm);
		border: 1px solid var(--border);
		background: var(--surface-subtle);
		cursor: pointer;
	}

	.color-picker-pill input[type='color'] {
		width: 28px;
		height: 28px;
		padding: 0;
		border: none;
		background: transparent;
		cursor: pointer;
	}

	.preset-swatches {
		display: flex;
		flex-wrap: wrap;
		gap: 8px;
	}

	.swatch-btn {
		width: 26px;
		height: 26px;
		padding: 0;
		border-radius: 50%;
		border: 2px solid var(--border);
		transition: transform 0.1s ease;
	}

	.swatch-btn:hover {
		transform: scale(1.12);
	}

	.swatch-btn.selected {
		border-color: var(--text);
		box-shadow: 0 0 0 3px var(--accent-soft);
	}

	.url-row {
		display: flex;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.url-row .input {
		flex: 1;
		min-width: 200px;
	}

	.test-result {
		padding: var(--space-xs) var(--space-sm);
		border-radius: var(--radius-sm);
		font-size: 0.88em;
		border: 1px solid var(--border);
	}

	.test-result.ok {
		background: var(--success-soft);
		border-color: var(--success-border);
		color: var(--success);
	}

	.test-result.err {
		background: var(--error-soft);
		border-color: var(--error-border);
		color: var(--error);
	}

	.limit-input {
		width: 88px;
		text-align: center;
	}

	.divider {
		height: 1px;
		background: var(--border);
	}

	@media (max-width: 480px) {
		.settings-grid {
			grid-template-columns: 1fr;
		}
	}
</style>