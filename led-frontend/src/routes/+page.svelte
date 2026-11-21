<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import EffectForm from '$lib/components/EffectForm.svelte';
	import HistorySidebar from '$lib/components/HistorySidebar.svelte';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { toasts } from '$lib/stores/toasts.svelte.js';
	import { buildInitialEffectState } from '$lib/utils/typeParser.js';

	let selectedId = $state('');
	let paramValues = $state({});
	let linkedLengths = $state({});
	let linkedVars = $state([]);
	let initialized = $state(false);

	onMount(() => {
		effectsStore.load();
	});

	function selectEffect(effectId, seedParams = null) {
		const effect = effectsStore.byId[effectId];
		if (!effect) return false;

		const state = buildInitialEffectState(effect, seedParams);
		selectedId = effect.id;
		paramValues = state.values;
		linkedLengths = state.linkedLengths;
		linkedVars = state.linkedVars;
		return true;
	}

	// Initialize once effects are loaded (honoring /effects handoff, ?effect= query, fill-rgb, or first effect)
	$effect(() => {
		if (initialized || effectsStore.list.length === 0) return;

		const queued = effectsStore.consumeQueuedEffect();
		const queryId = $page.url.searchParams.get('effect');
		const preferred = queued || queryId;

		if (preferred && effectsStore.byId[preferred]) {
			selectEffect(preferred);
			if (queued) {
				toasts.info('Loaded Defaults', `Populated "${effectsStore.byId[preferred].name}" with default values.`);
			}
		} else {
			selectEffect(effectsStore.defaultEffectId);
		}

		initialized = true;
	});

	// If a refresh removes the currently selected effect, fall back cleanly
	$effect(() => {
		if (!initialized || effectsStore.list.length === 0) return;
		if (selectedId && !effectsStore.byId[selectedId]) {
			selectEffect(effectsStore.defaultEffectId);
		}
	});

	function handleUpdateParam(varname, nextVal) {
		paramValues = {
			...paramValues,
			[varname]: nextVal
		};
	}

	function handleUpdateLinked(nextLengths, nextValues) {
		linkedLengths = nextLengths;
		paramValues = nextValues;
	}

	function handleResetDefaults() {
		if (!selectedId) return;
		selectEffect(selectedId);
		toasts.info('Reset to Defaults', `Restored default parameters for "${effectsStore.byId[selectedId]?.name ?? selectedId}".`);
	}

	function handleLoadHistoryEntry(entry) {
		if (!effectsStore.byId[entry.id]) {
			toasts.error(
				'Effect Not Available',
				`"${entry.name}" (${entry.id}) is not currently advertised by the server.`
			);
			return;
		}
		selectEffect(entry.id, entry.params);
		toasts.info('Loaded from History', `Loaded "${entry.name}" into the editor.`);
	}
</script>

<svelte:head>
	<title>Runner · Pi-Tree Controller</title>
</svelte:head>

<div class="runner-grid">
	<div class="primary-col">
		<EffectForm
			{selectedId}
			{paramValues}
			{linkedLengths}
			{linkedVars}
			onSelectEffect={(id) => selectEffect(id)}
			onUpdateParam={handleUpdateParam}
			onUpdateLinked={handleUpdateLinked}
			onResetDefaults={handleResetDefaults}
		/>
	</div>

	<div class="sidebar-col">
		<HistorySidebar onLoadEntry={handleLoadHistoryEntry} />
	</div>
</div>

<style>
	.runner-grid {
		display: grid;
		grid-template-columns: minmax(0, 1fr) 360px;
		gap: var(--space-lg);
		align-items: start;
	}

	.primary-col,
	.sidebar-col {
		min-width: 0;
	}

	@media (max-width: 980px) {
		.runner-grid {
			grid-template-columns: 1fr;
		}
	}
</style>