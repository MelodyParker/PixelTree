<script>
	import { onMount } from 'svelte';
	import EffectDetailCard from '$lib/components/EffectDetailCard.svelte';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { settings } from '$lib/stores/settings.svelte.js';

	let search = $state('');

	onMount(() => {
		effectsStore.load();
	});

	let filteredEffects = $derived.by(() => {
		const q = search.trim().toLowerCase();
		if (!q) return effectsStore.list;
		return effectsStore.list.filter((effect) => {
			if (effect.id.toLowerCase().includes(q)) return true;
			if (effect.name.toLowerCase().includes(q)) return true;
			if (effect.description.toLowerCase().includes(q)) return true;
			return effect.params.some(
				(p) =>
					p.name.toLowerCase().includes(q) ||
					p.varname.toLowerCase().includes(q) ||
					p.type.toLowerCase().includes(q)
			);
		});
	});
</script>

<svelte:head>
	<title>Effects Explorer · Pi-Tree Controller</title>
</svelte:head>

<div class="explorer-page">
	<header class="explorer-header card">
		<div class="header-top">
			<div>
				<h1>Effects Explorer</h1>
				<p class="muted subtitle">
					Full schema breakdown of all effects returned by <span class="mono">{settings.apiBaseUrl}/api/effects</span>.
				</p>
			</div>
			<button
				type="button"
				class="btn btn-sm"
				disabled={effectsStore.loading}
				onclick={() => effectsStore.load(true)}
			>
				{effectsStore.loading ? 'Refreshing…' : '↻ Refresh'}
			</button>
		</div>

		<div class="toolbar">
			<input
				type="search"
				class="input search-input"
				placeholder="Filter by effect name, ID, parameter, or type (e.g., list_N, color)…"
				bind:value={search}
			/>
			<span class="badge">
				Showing {filteredEffects.length} of {effectsStore.list.length}
			</span>
		</div>
	</header>

	{#if effectsStore.loading && !effectsStore.loaded}
		<div class="card empty-state">Loading effects from server…</div>
	{:else if effectsStore.error && !effectsStore.loaded}
		<div class="card empty-state error-state">
			<strong>Could not load effects</strong>
			<p class="muted">{effectsStore.error}</p>
			<div class="actions">
				<button type="button" class="btn btn-primary btn-sm" onclick={() => effectsStore.load(true)}>
					Retry
				</button>
				<a href="/settings" class="btn btn-sm">Open Settings</a>
			</div>
		</div>
	{:else if filteredEffects.length === 0}
		<div class="card empty-state">
			<p class="muted">No effects match "{search}".</p>
			{#if search}
				<button type="button" class="btn btn-sm" onclick={() => (search = '')}>
					Clear Search
				</button>
			{/if}
		</div>
	{:else}
		<div class="cards-stack">
			{#each filteredEffects as effect (effect.id)}
				<EffectDetailCard {effect} />
			{/each}
		</div>
	{/if}
</div>

<style>
	.explorer-page {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.explorer-header {
		padding: var(--space-lg);
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.header-top {
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

	.toolbar {
		display: flex;
		align-items: center;
		gap: var(--space-sm);
		flex-wrap: wrap;
	}

	.search-input {
		flex: 1;
		min-width: 220px;
	}

	.cards-stack {
		display: flex;
		flex-direction: column;
		gap: var(--space-md);
	}

	.empty-state {
		padding: var(--space-lg);
		display: flex;
		flex-direction: column;
		align-items: flex-start;
		gap: var(--space-sm);
	}

	.error-state {
		border-color: var(--error-border);
		background: var(--error-soft);
	}

	.actions {
		display: flex;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}
</style>