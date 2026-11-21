import { browser } from '$app/environment';
import { normalizeBaseUrl } from '$lib/api/client.js';

const STORAGE_KEY = 'pi_tree_settings_v1';

export const DEFAULT_SETTINGS = {
	theme: 'dark', // 'dark' | 'light'
	accentColor: '#38bdf8',
	borderRadius: 'balanced', // 'sharp' | 'balanced' | 'rounded'
	density: 'comfortable', // 'compact' | 'comfortable' | 'spacious'
	historyLimit: 10,
	apiBaseUrl: 'http://pi-tree:5000'
};

export const ACCENT_PRESETS = [
	{ name: 'Sky', hex: '#38bdf8' },
	{ name: 'Emerald', hex: '#10b981' },
	{ name: 'Festive Red', hex: '#ef4444' },
	{ name: 'Amber', hex: '#f59e0b' },
	{ name: 'Violet', hex: '#a855f7' },
	{ name: 'Rose', hex: '#f43f5e' },
	{ name: 'Indigo', hex: '#6366f1' },
	{ name: 'Teal', hex: '#14b8a6' }
];

function loadFromStorage() {
	if (!browser) return { ...DEFAULT_SETTINGS };
	try {
		const raw = localStorage.getItem(STORAGE_KEY);
		if (!raw) return { ...DEFAULT_SETTINGS };
		const parsed = JSON.parse(raw);
		return {
			theme: parsed.theme === 'light' ? 'light' : 'dark',
			accentColor:
				typeof parsed.accentColor === 'string' && /^#[0-9a-fA-F]{6}$/.test(parsed.accentColor)
					? parsed.accentColor
					: DEFAULT_SETTINGS.accentColor,
			borderRadius: ['sharp', 'balanced', 'rounded'].includes(parsed.borderRadius)
				? parsed.borderRadius
				: DEFAULT_SETTINGS.borderRadius,
			density: ['compact', 'comfortable', 'spacious'].includes(parsed.density)
				? parsed.density
				: DEFAULT_SETTINGS.density,
			historyLimit:
				Number.isInteger(parsed.historyLimit) && parsed.historyLimit >= 1 && parsed.historyLimit <= 100
					? parsed.historyLimit
					: DEFAULT_SETTINGS.historyLimit,
			apiBaseUrl:
				typeof parsed.apiBaseUrl === 'string' && parsed.apiBaseUrl.trim()
					? normalizeBaseUrl(parsed.apiBaseUrl)
					: DEFAULT_SETTINGS.apiBaseUrl
		};
	} catch {
		return { ...DEFAULT_SETTINGS };
	}
}

class SettingsStore {
	theme = $state(DEFAULT_SETTINGS.theme);
	accentColor = $state(DEFAULT_SETTINGS.accentColor);
	borderRadius = $state(DEFAULT_SETTINGS.borderRadius);
	density = $state(DEFAULT_SETTINGS.density);
	historyLimit = $state(DEFAULT_SETTINGS.historyLimit);
	apiBaseUrl = $state(DEFAULT_SETTINGS.apiBaseUrl);

	constructor() {
		const initial = loadFromStorage();
		this.theme = initial.theme;
		this.accentColor = initial.accentColor;
		this.borderRadius = initial.borderRadius;
		this.density = initial.density;
		this.historyLimit = initial.historyLimit;
		this.apiBaseUrl = initial.apiBaseUrl;
	}

	save() {
		if (!browser) return;
		try {
			localStorage.setItem(
				STORAGE_KEY,
				JSON.stringify({
					theme: this.theme,
					accentColor: this.accentColor,
					borderRadius: this.borderRadius,
					density: this.density,
					historyLimit: this.historyLimit,
					apiBaseUrl: this.apiBaseUrl
				})
			);
		} catch {
			// Ignore storage quota errors
		}
	}

	toggleTheme() {
		this.theme = this.theme === 'dark' ? 'light' : 'dark';
		this.save();
	}

	setTheme(theme) {
		if (theme !== 'dark' && theme !== 'light') return;
		this.theme = theme;
		this.save();
	}

	setAccentColor(hex) {
		if (typeof hex !== 'string' || !/^#[0-9a-fA-F]{6}$/.test(hex)) return;
		this.accentColor = hex;
		this.save();
	}

	setBorderRadius(radius) {
		if (!['sharp', 'balanced', 'rounded'].includes(radius)) return;
		this.borderRadius = radius;
		this.save();
	}

	setDensity(density) {
		if (!['compact', 'comfortable', 'spacious'].includes(density)) return;
		this.density = density;
		this.save();
	}

	setHistoryLimit(limit) {
		const parsed = Math.max(1, Math.min(100, Math.round(Number(limit) || DEFAULT_SETTINGS.historyLimit)));
		this.historyLimit = parsed;
		this.save();
	}

	setApiBaseUrl(url) {
		const normalized = normalizeBaseUrl(url);
		if (!normalized) return;
		this.apiBaseUrl = normalized;
		this.save();
	}

	reset() {
		this.theme = DEFAULT_SETTINGS.theme;
		this.accentColor = DEFAULT_SETTINGS.accentColor;
		this.borderRadius = DEFAULT_SETTINGS.borderRadius;
		this.density = DEFAULT_SETTINGS.density;
		this.historyLimit = DEFAULT_SETTINGS.historyLimit;
		this.apiBaseUrl = DEFAULT_SETTINGS.apiBaseUrl;
		this.save();
	}
}

export const settings = new SettingsStore();