<script>
	import { goto } from '$app/navigation';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { rgbToCss } from '$lib/utils/color.js';
	import {
		buildInitialEffectState,
		describeType,
		parseDefaultValue
	} from '$lib/utils/typeParser.js';
	import TypeTree from './TypeTree.svelte';

	let { effect } = $props();

	let showPayload = $state(false);

	let initialState = $derived(buildInitialEffectState(effect));

	let defaultPayload = $derived({
		id: effect.id,
		...initialState.values
	});

	function handleLoadInRunner() {
		effectsStore.queueEffect(effect.id);
		goto(`/?effect=${encodeURIComponent(effect.id)}`);
	}
</script>

<article class="card detail-card">
	<header class="detail-head">
		<div class="title-block">
			<div class="title-row">
				<h2>{effect.name}</h2>
				<span class="badge mono">{effect.id}</span>
				<span class="badge">
					{effect.params.length} {effect.params.length === 1 ? 'parameter' : 'parameters'}
				</span>
				{#each initialState.linkedVars as varName}
					<span class="badge badge-accent mono">linked: {varName}</span>
				{/each}
			</div>
			{#if effect.description}
				<p class="desc muted">{effect.description}</p>
			{/if}
		</div>

		<button type="button" class="btn btn-primary" onclick={handleLoadInRunner}>
			Load Defaults in Runner →
		</button>
	</header>

	{#if effect.params.length === 0}
		<div class="no-params muted">
			This effect requires no parameters.
		</div>
	{:else}
		<div class="param-grid">
			{#each effect.params as param (param.varname)}
				{@const resolved = parseDefaultValue(param.ast, param.default, initialState.linkedLengths)}
				<div class="param-card">
					<div class="param-top">
						<div>
							<div class="param-title">{param.name}</div>
							<div class="param-sub muted">{describeType(param.ast)}</div>
						</div>
						<div class="param-tags">
							<span class="badge mono">varname: {param.varname}</span>
							<span class="badge badge-accent mono">{param.type}</span>
						</div>
					</div>

					<div class="tree-section">
						<div class="sub-label">Type Structure</div>
						<TypeTree node={param.ast} />
					</div>

					<div class="default-section">
						<div class="default-head">
							<span class="sub-label">Default Value</span>
							{#if resolved.usedServerDefault}
								<span class="badge badge-success">Server Default</span>
							{:else}
								<span class="badge badge-warning">Client Fallback</span>
							{/if}
						</div>

						<div class="default-value-row">
							{#if param.ast.kind === 'color'}
								<span
									class="swatch"
									style:background={rgbToCss(resolved.value)}
									aria-hidden="true"
								></span>
							{/if}
							<code class="default-code">{JSON.stringify(resolved.value)}</code>
							{#if resolved.usedServerDefault && param.default !== undefined}
								<span class="raw-note muted mono">(raw: {JSON.stringify(param.default)})</span>
							{/if}
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}

	<footer class="detail-foot">
		<button
			type="button"
			class="btn btn-ghost btn-sm mono"
			onclick={() => (showPayload = !showPayload)}
		>
			{showPayload ? '▾ Hide Default POST Payload' : '▸ Show Default POST Payload'}
		</button>

		{#if showPayload}
			<pre class="payload-pre">{JSON.stringify(defaultPayload, null, 2)}</pre>
		{/if}
	</footer>
</article>

<style>
	.detail-card {
		padding: var(--space-lg);
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.detail-head {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	.title-block {
		display: flex;
		flex-direction: column;
		gap: 6px;
		flex: 1;
		min-width: 240px;
	}

	.title-row {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	h2 {
		font-size: 1.25em;
		letter-spacing: -0.01em;
	}

	.desc {
		font-size: 0.94em;
	}

	.no-params {
		padding: var(--space-md);
		border-radius: var(--radius-md);
		background: var(--surface-subtle);
		border: 1px dashed var(--border);
		font-size: 0.92em;
	}

	.param-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		gap: var(--space-md);
	}

	.param-card {
		padding: var(--space-md);
		border-radius: var(--radius-md);
		background: var(--surface-subtle);
		border: 1px solid var(--border);
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
	}

	.param-top {
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.param-title {
		font-weight: 600;
	}

	.param-sub {
		font-size: 0.82em;
		margin-top: 2px;
	}

	.param-tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
	}

	.sub-label {
		font-size: 0.76em;
		font-weight: 700;
		text-transform: uppercase;
		letter-spacing: 0.05em;
		color: var(--text-dim);
	}

	.tree-section {
		display: flex;
		flex-direction: column;
		gap: 6px;
		padding: var(--space-sm);
		border-radius: var(--radius-sm);
		background: var(--surface);
		border: 1px solid var(--border);
	}

	.default-section {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.default-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-xs);
	}

	.default-value-row {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
		padding: 6px 10px;
		border-radius: var(--radius-sm);
		background: var(--surface);
		border: 1px solid var(--border);
	}

	.swatch {
		width: 14px;
		height: 14px;
		border-radius: 4px;
		border: 1px solid var(--border-strong);
		flex-shrink: 0;
	}

	.default-code {
		font-size: 0.88em;
		word-break: break-all;
	}

	.raw-note {
		font-size: 0.8em;
	}

	.detail-foot {
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: var(--space-xs);
		padding-top: var(--space-xs);
		border-top: 1px solid var(--border);
	}

	.payload-pre {
		width: 100%;
		margin: 0;
		padding: var(--space-sm) var(--space-md);
		border-radius: var(--radius-sm);
		background: var(--surface-subtle);
		border: 1px solid var(--border);
		font-size: 0.85em;
		overflow-x: auto;
	}
</style>