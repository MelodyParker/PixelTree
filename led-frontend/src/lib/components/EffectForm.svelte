<script>
	import { runEffect } from '$lib/api/client.js';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { historyStore } from '$lib/stores/history.svelte.js';
	import { settings } from '$lib/stores/settings.svelte.js';
	import { toasts } from '$lib/stores/toasts.svelte.js';
	import {
		clonePlain,
		resizeLinkedListsInValue
	} from '$lib/utils/typeParser.js';
	import ParamInput from './params/ParamInput.svelte';

	let {
		selectedId = '',
		paramValues = {},
		linkedLengths = {},
		linkedVars = [],
		onSelectEffect,
		onUpdateParam,
		onUpdateLinked,
		onResetDefaults
	} = $props();

	let sending = $state(false);
	let showPayload = $state(false);

	let selectedEffect = $derived(effectsStore.byId[selectedId] ?? null);

	let payloadPreview = $derived.by(() => {
		if (!selectedEffect) return {};
		const payload = { id: selectedEffect.id };
		for (const param of selectedEffect.params) {
			payload[param.varname] = clonePlain(paramValues[param.varname]);
		}
		return payload;
	});

	function handleSelectChange(event) {
		onSelectEffect(event.currentTarget.value);
	}

	function handleResizeLinked(varName, nextLength, removeIndex = null) {
		if (!selectedEffect) return;
		const clamped = Math.max(1, Math.floor(Number(nextLength) || 1));
		const nextLengths = { ...linkedLengths, [varName]: clamped };
		const nextValues = {};

		for (const param of selectedEffect.params) {
			nextValues[param.varname] = resizeLinkedListsInValue(
				param.ast,
				paramValues[param.varname],
				varName,
				clamped,
				nextLengths,
				removeIndex
			);
		}

		onUpdateLinked(nextLengths, nextValues);
	}

	async function handleSubmit(event) {
		event.preventDefault();
		if (!selectedEffect || sending) return;

		sending = true;
		const payload = clonePlain(payloadPreview);

		try {
			const result = await runEffect(settings.apiBaseUrl, payload);
			const savedParams = {};
			for (const param of selectedEffect.params) {
				savedParams[param.varname] = payload[param.varname];
			}

			historyStore.recordRun({
				id: selectedEffect.id,
				name: selectedEffect.name,
				params: savedParams
			});

			toasts.success(
				`Running: ${selectedEffect.name}`,
				result.message || `Effect "${selectedEffect.id}" acknowledged by server.`
			);
		} catch (err) {
			toasts.error(`Failed to run "${selectedEffect.name}"`, err.message);
		} finally {
			sending = false;
		}
	}
</script>

<section class="card form-card">
	<div class="card-header">
		<div>
			<h1>Effect Controller</h1>
			<p class="muted subtitle">Select an effect, tune its parameters, and send it to the tree.</p>
		</div>
		<button
			type="button"
			class="btn btn-sm"
			disabled={effectsStore.loading}
			onclick={() => effectsStore.load(true)}
		>
			{effectsStore.loading ? 'Refreshing…' : '↻ Refresh Effects'}
		</button>
	</div>

	{#if effectsStore.loading && !effectsStore.loaded}
		<div class="state-box">
			<p>Fetching available effects from <span class="mono">{settings.apiBaseUrl}/api/effects</span>…</p>
		</div>
	{:else if effectsStore.error && !effectsStore.loaded}
		<div class="state-box error-box">
			<p><strong>Unable to load effects</strong></p>
			<p class="muted">{effectsStore.error}</p>
			<div class="state-actions">
				<button type="button" class="btn btn-primary btn-sm" onclick={() => effectsStore.load(true)}>
					Retry
				</button>
				<a href="/settings" class="btn btn-sm">Check API URL in Settings</a>
			</div>
		</div>
	{:else if effectsStore.list.length === 0}
		<div class="state-box">
			<p class="muted">No effects were returned by the server.</p>
		</div>
	{:else}
		<form class="effect-form" onsubmit={handleSubmit}>
			<div class="selector-group">
				<label for="effect-select" class="field-label">
					<span>Effect</span>
					{#if selectedEffect}
						<span class="mono muted id-tag">id: {selectedEffect.id}</span>
					{/if}
				</label>
				<select
					id="effect-select"
					class="select effect-select"
					value={selectedId}
					onchange={handleSelectChange}
				>
					{#each effectsStore.list as effect (effect.id)}
						<option value={effect.id}>
							{effect.name} ({effect.id})
						</option>
					{/each}
				</select>
				{#if selectedEffect?.description}
					<p class="effect-desc muted">{selectedEffect.description}</p>
				{/if}
			</div>

			{#if selectedEffect}
				{#if linkedVars.length > 0}
					<div class="linked-bar">
						<div class="linked-title">
							<span class="badge badge-accent">Linked List Lengths</span>
							<span class="muted">Parameters sharing a length variable resize together.</span>
						</div>
						<div class="linked-controls">
							{#each linkedVars as varName (varName)}
								<div class="linked-pill">
									<span class="mono var-label">{varName} =</span>
									<button
										type="button"
										class="btn btn-sm btn-icon"
										disabled={(linkedLengths[varName] ?? 1) <= 1}
										onclick={() => handleResizeLinked(varName, (linkedLengths[varName] ?? 1) - 1)}
										aria-label={`Decrease linked length ${varName}`}
									>
										−
									</button>
									<span class="mono var-count">{linkedLengths[varName] ?? 1}</span>
									<button
										type="button"
										class="btn btn-sm btn-icon"
										onclick={() => handleResizeLinked(varName, (linkedLengths[varName] ?? 1) + 1)}
										aria-label={`Increase linked length ${varName}`}
									>
										+
									</button>
								</div>
							{/each}
						</div>
					</div>
				{/if}

				{#if selectedEffect.params.length === 0}
					<div class="no-params">
						<span class="muted">This effect takes no parameters — ready to run!</span>
					</div>
				{:else}
					<div class="params-list">
						{#each selectedEffect.params as param (selectedEffect.id + ':' + param.varname)}
							<div class="param-block">
								<div class="param-header">
									<label for={`param-${param.varname}`} class="param-name">
										{param.name}
									</label>
									<div class="param-badges">
										<span class="badge mono">{param.varname}</span>
										<span class="badge badge-accent mono">{param.type}</span>
										{#if param.default !== undefined}
											<span class="badge">default: {String(param.default)}</span>
										{/if}
									</div>
								</div>

								{#if param.parseError}
									<p class="parse-warn">Type parse warning: {param.parseError}</p>
								{/if}

								<ParamInput
									id={`param-${param.varname}`}
									ariaLabel={param.name}
									node={param.ast}
									value={paramValues[param.varname]}
									onchange={(nextVal) => onUpdateParam(param.varname, nextVal)}
									{linkedLengths}
									onResizeLinked={handleResizeLinked}
								/>
							</div>
						{/each}
					</div>
				{/if}

				<div class="form-footer">
					<div class="footer-left">
						<button type="submit" class="btn btn-primary run-btn" disabled={sending}>
							{sending ? 'Sending…' : '▶ Start Effect'}
						</button>
						<button type="button" class="btn" onclick={onResetDefaults}>
							Reset Defaults
						</button>
					</div>

					<button
						type="button"
						class="btn btn-ghost btn-sm mono"
						onclick={() => (showPayload = !showPayload)}
					>
						{showPayload ? 'Hide JSON' : '{ } Preview JSON'}
					</button>
				</div>

				{#if showPayload}
					<div class="payload-box">
						<div class="payload-header mono muted">
							POST {settings.apiBaseUrl}/effect/run
						</div>
						<pre class="payload-pre">{JSON.stringify(payloadPreview, null, 2)}</pre>
					</div>
				{/if}
			{/if}
		</form>
	{/if}
</section>

<style>
	.form-card {
		padding: var(--space-lg);
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.card-header {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	h1 {
		font-size: 1.45em;
		letter-spacing: -0.02em;
	}

	.subtitle {
		margin-top: 2px;
		font-size: 0.92em;
	}

	.state-box {
		padding: var(--space-lg);
		border-radius: var(--radius-md);
		border: 1px dashed var(--border-strong);
		background: var(--surface-elevated);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
	}

	.error-box {
		border-color: var(--error-border);
		background: var(--error-soft);
	}

	.state-actions {
		display: flex;
		gap: var(--space-xs);
		flex-wrap: wrap;
		margin-top: var(--space-xs);
	}

	.effect-form {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.selector-group {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	.field-label {
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-weight: 600;
	}

	.id-tag {
		font-size: 0.85em;
		font-weight: 400;
	}

	.effect-select {
		font-weight: 600;
	}

	.effect-desc {
		font-size: 0.92em;
	}

	.linked-bar {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-md);
		border-radius: var(--radius-md);
		border: 1px solid var(--accent-border);
		background: var(--accent-soft);
	}

	.linked-title {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		flex-wrap: wrap;
		font-size: 0.9em;
	}

	.linked-controls {
		display: flex;
		flex-wrap: wrap;
		gap: var(--space-sm);
	}

	.linked-pill {
		display: inline-flex;
		align-items: center;
		gap: var(--space-xs);
		padding: 4px 8px;
		border-radius: var(--radius-sm);
		background: var(--surface);
		border: 1px solid var(--border);
	}

	.var-label {
		font-weight: 600;
		font-size: 0.9em;
	}

	.var-count {
		min-width: 24px;
		text-align: center;
		font-weight: 700;
	}

	.no-params {
		padding: var(--space-md);
		border-radius: var(--radius-md);
		background: var(--surface-elevated);
		border: 1px dashed var(--border);
		text-align: center;
	}

	.params-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.param-block {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		padding: var(--space-md);
		border-radius: var(--radius-md);
		border: 1px solid var(--border);
		background: var(--surface-subtle);
	}

	.param-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.param-name {
		font-weight: 600;
	}

	.param-badges {
		display: flex;
		align-items: center;
		gap: 6px;
		flex-wrap: wrap;
	}

	.parse-warn {
		font-size: 0.85em;
		color: var(--warning);
	}

	.form-footer {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-sm);
		flex-wrap: wrap;
		padding-top: var(--space-sm);
		border-top: 1px solid var(--border);
	}

	.footer-left {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.run-btn {
		min-width: 150px;
	}

	.payload-box {
		border-radius: var(--radius-md);
		border: 1px solid var(--border);
		background: var(--surface-subtle);
		overflow: hidden;
	}

	.payload-header {
		padding: 6px var(--space-sm);
		font-size: 0.82em;
		border-bottom: 1px solid var(--border);
		background: var(--surface-elevated);
	}

	.payload-pre {
		margin: 0;
		padding: var(--space-sm) var(--space-md);
		font-size: 0.85em;
		overflow-x: auto;
	}
</style>