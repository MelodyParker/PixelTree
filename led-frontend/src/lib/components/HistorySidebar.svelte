<script>
	import { runEffect } from '$lib/api/client.js';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { historyStore } from '$lib/stores/history.svelte.js';
	import { settings } from '$lib/stores/settings.svelte.js';
	import { toasts } from '$lib/stores/toasts.svelte.js';
	import { rgbToCss } from '$lib/utils/color.js';
	import { clonePlain, isRgbTuple } from '$lib/utils/typeParser.js';

	let { onLoadEntry } = $props();

	let rerunningUid = $state(null);

	function formatTime(ts) {
		if (!ts) return '';
		return new Date(ts).toLocaleTimeString([], {
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit'
		});
	}

	function getParamMeta(effectId, varname) {
		const effect = effectsStore.byId[effectId];
		if (!effect) return null;
		return effect.params.find((p) => p.varname === varname) ?? null;
	}

	async function handleRunAgain(entry) {
		if (rerunningUid) return;
		rerunningUid = entry.uid;

		const payload = {
			id: entry.id,
			...clonePlain(entry.params ?? {})
		};

		try {
			const res = await runEffect(settings.apiBaseUrl, payload);
			historyStore.recordRun({
				id: entry.id,
				name: effectsStore.byId[entry.id]?.name ?? entry.name,
				params: entry.params
			});
			toasts.success(
				`Re-ran: ${entry.name}`,
				res.message || `Effect "${entry.id}" acknowledged by server.`
			);
		} catch (err) {
			toasts.error(`Failed to re-run "${entry.name}"`, err.message);
		} finally {
			rerunningUid = null;
		}
	}
</script>

{#snippet renderValue(val, ast)}
	{#if ast?.kind === 'color' || (!ast && isRgbTuple(val))}
		<span class="color-chip">
			<span class="dot" style:background={rgbToCss(val)}></span>
			<span class="mono">[{Array.isArray(val) ? val.join(', ') : val}]</span>
		</span>
	{:else if typeof val === 'boolean'}
		<span class="badge" class:badge-success={val}>{val ? 'true' : 'false'}</span>
	{:else if Array.isArray(val)}
		<span class="list-chip">
			{#each val as item, i}
				{@render renderValue(item, ast?.kind === 'list' ? ast.itemType : null)}{#if i < val.length - 1}<span class="sep">,</span>{/if}
			{/each}
		</span>
	{:else}
		<span class="mono">{String(val)}</span>
	{/if}
{/snippet}

<aside class="sidebar">
	<!-- Currently Running Effect -->
	<section class="card sidebar-card">
		<div class="section-head">
			<h2>Currently Running</h2>
			{#if historyStore.active}
				<span class="badge badge-success">Active</span>
			{:else}
				<span class="badge">Idle</span>
			{/if}
		</div>

		{#if historyStore.active}
			{@const active = historyStore.active}
			{@const paramEntries = Object.entries(active.params ?? {})}
			<div class="active-body">
				<div class="active-title-row">
					<strong>{active.name}</strong>
					<span class="mono muted small">{active.id}</span>
				</div>
				<div class="muted small">Sent at {formatTime(active.ranAt)}</div>

				{#if paramEntries.length === 0}
					<div class="empty-inline muted">No parameters</div>
				{:else}
					<dl class="param-dl">
						{#each paramEntries as [key, val]}
							{@const meta = getParamMeta(active.id, key)}
							<div class="param-kv">
								<dt>{meta?.name ?? key}</dt>
								<dd>{@render renderValue(val, meta?.ast ?? null)}</dd>
							</div>
						{/each}
					</dl>
				{/if}

				<div class="entry-actions">
					<button type="button" class="btn btn-sm" onclick={() => onLoadEntry(active)}>
						Load in Editor
					</button>
					<button
						type="button"
						class="btn btn-sm btn-primary"
						disabled={rerunningUid !== null}
						onclick={() => handleRunAgain(active)}
					>
						{rerunningUid === active.uid ? 'Sending…' : '↻ Re-send'}
					</button>
				</div>
			</div>
		{:else}
			<p class="muted small">
				No effect has been launched from this browser yet. Run an effect to track its active state here.
			</p>
		{/if}
	</section>

	<!-- Recent History -->
	<section class="card sidebar-card">
		<div class="section-head">
			<div class="head-left">
				<h2>Recent History</h2>
				<span class="badge">{historyStore.entries.length}/{settings.historyLimit}</span>
			</div>
			{#if historyStore.entries.length > 0}
				<button
					type="button"
					class="btn btn-ghost btn-sm"
					onclick={() => historyStore.clearHistory()}
				>
					Clear
				</button>
			{/if}
		</div>

		{#if historyStore.entries.length === 0}
			<p class="muted small">Your last {settings.historyLimit} effect runs will appear here.</p>
		{:else}
			<div class="history-list">
				{#each historyStore.entries as entry (entry.uid)}
					{@const paramEntries = Object.entries(entry.params ?? {})}
					<article class="history-item">
						<div class="history-top">
							<div class="history-name">
								<strong>{entry.name}</strong>
								<span class="muted small">{formatTime(entry.ranAt)}</span>
							</div>
							<button
								type="button"
								class="remove-x"
								onclick={() => historyStore.removeEntry(entry.uid)}
								title="Remove from history"
								aria-label="Remove entry"
							>
								×
							</button>
						</div>

						{#if paramEntries.length > 0}
							<div class="history-params">
								{#each paramEntries as [key, val]}
									{@const meta = getParamMeta(entry.id, key)}
									<div class="mini-param">
										<span class="muted mono">{key}:</span>
										{@render renderValue(val, meta?.ast ?? null)}
									</div>
								{/each}
							</div>
						{:else}
							<div class="muted small">No parameters</div>
						{/if}

						<div class="entry-actions">
							<button type="button" class="btn btn-sm" onclick={() => onLoadEntry(entry)}>
								Load
							</button>
							<button
								type="button"
								class="btn btn-sm btn-primary"
								disabled={rerunningUid !== null}
								onclick={() => handleRunAgain(entry)}
							>
								{rerunningUid === entry.uid ? 'Sending…' : '▶ Run'}
							</button>
						</div>
					</article>
				{/each}
			</div>
		{/if}
	</section>
</aside>

<style>
	.sidebar {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.sidebar-card {
		padding: var(--space-md);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
	}

	.section-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-xs);
	}

	.head-left {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
	}

	h2 {
		font-size: 1.05em;
	}

	.small {
		font-size: 0.85em;
	}

	.active-body {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	.active-title-row {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.empty-inline {
		font-size: 0.86em;
		padding: var(--space-xs) 0;
	}

	.param-dl {
		margin: var(--space-xs) 0;
		padding: var(--space-sm);
		border-radius: var(--radius-sm);
		background: var(--surface-subtle);
		border: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.param-kv {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	dt {
		font-size: 0.8em;
		color: var(--text-muted);
		font-weight: 600;
	}

	dd {
		margin: 0;
		font-size: 0.86em;
		word-break: break-word;
	}

	.history-list {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		max-height: 540px;
		overflow-y: auto;
		padding-right: 2px;
	}

	.history-item {
		padding: var(--space-sm);
		border-radius: var(--radius-md);
		background: var(--surface-elevated);
		border: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	.history-top {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: var(--space-xs);
	}

	.history-name {
		display: flex;
		flex-direction: column;
	}

	.remove-x {
		background: transparent;
		border: none;
		color: var(--text-dim);
		font-size: 1.15em;
		line-height: 1;
		padding: 0 4px;
	}

	.remove-x:hover {
		color: var(--error);
	}

	.history-params {
		display: flex;
		flex-direction: column;
		gap: 4px;
		font-size: 0.82em;
		padding: 6px 8px;
		border-radius: var(--radius-sm);
		background: var(--surface);
		border: 1px solid var(--border);
	}

	.mini-param {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 4px;
	}

	.entry-actions {
		display: flex;
		gap: var(--space-xs);
		margin-top: 2px;
	}

	.entry-actions .btn {
		flex: 1;
	}

	.color-chip {
		display: inline-flex;
		align-items: center;
		gap: 5px;
		padding: 1px 6px;
		border-radius: 999px;
		border: 1px solid var(--border);
		background: var(--surface-elevated);
		font-size: 0.92em;
	}

	.dot {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		border: 1px solid rgba(128, 128, 128, 0.5);
		flex-shrink: 0;
	}

	.list-chip {
		display: inline-flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 4px;
	}

	.sep {
		color: var(--text-dim);
		margin-right: 2px;
	}
</style>