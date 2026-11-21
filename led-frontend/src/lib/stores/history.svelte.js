import { browser } from '$app/environment';
import { clonePlain } from '$lib/utils/typeParser.js';
import { settings } from './settings.svelte.js';

const STORAGE_KEY = 'pi_tree_history_v1';

function loadFromStorage() {
	if (!browser) return { active: null, entries: [] };
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		if (!raw) return { active: null, entries: [] };
		const parsed = JSON.parse(raw);
		return {
			active: parsed?.active && typeof parsed.active === 'object' ? parsed.active : null,
			entries: Array.isArray(parsed?.entries) ? parsed.entries : []
		};
	} catch {
		return { active: null, entries: [] };
	}
}

class HistoryStore {
	active = $state(null);
	entries = $state([]);

	constructor() {
		const initial = loadFromStorage();
		this.active = initial.active;
		this.entries = initial.entries.slice(0, settings.historyLimit);
	}

	save() {
		if (!browser) return;
		try {
			localStorage.setItem(
				STORAGE_KEY,
				JSON.stringify({
					active: this.active,
					entries: this.entries
				})
			);
		} catch {
			// Ignore storage quota errors
		}
	}

	recordRun({ id, name, params }) {
		const cleanParams = clonePlain(params ?? {});
		const record = {
			uid: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
			id,
			name: name || id,
			params: cleanParams,
			ranAt: Date.now()
		};

		this.active = clonePlain(record);
		this.entries = [record, ...this.entries].slice(0, settings.historyLimit);
		this.save();
	}

	trimToLimit(limit = settings.historyLimit) {
		if (this.entries.length > limit) {
			this.entries = this.entries.slice(0, limit);
			this.save();
		}
	}

	removeEntry(uid) {
		this.entries = this.entries.filter((item) => item.uid !== uid);
		this.save();
	}

	clearHistory() {
		this.entries = [];
		this.save();
	}

	clearAll() {
		this.active = null;
		this.entries = [];
		this.save();
	}
}

export const historyStore = new HistoryStore();