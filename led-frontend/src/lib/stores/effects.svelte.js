import { fetchEffects } from '$lib/api/client.js';
import { settings } from './settings.svelte.js';

class EffectsStore {
	byId = $state({});
	list = $state([]);
	loading = $state(false);
	loaded = $state(false);
	error = $state(null);
	lastFetchedAt = $state(null);

	// One-shot handoff when navigating from /effects ("Load Defaults in Runner") to /
	queuedEffectId = $state(null);

	get defaultEffectId() {
		if (this.byId['fill-rgb']) return 'fill-rgb';
		return this.list[0]?.id ?? '';
	}

	async load(force = false) {
		if (this.loading) return;
		if (this.loaded && !force) return;

		this.loading = true;
		this.error = null;

		try {
			const { byId, list } = await fetchEffects(settings.apiBaseUrl);
			this.byId = byId;
			this.list = list;
			this.loaded = true;
			this.lastFetchedAt = Date.now();
		} catch (err) {
			this.error = err.message || 'Failed to load effects from server.';
		} finally {
			this.loading = false;
		}
	}

	queueEffect(effectId) {
		this.queuedEffectId = effectId;
	}

	consumeQueuedEffect() {
		const id = this.queuedEffectId;
		this.queuedEffectId = null;
		return id;
	}
}

export const effectsStore = new EffectsStore();