<script>
	import { browser } from '$app/environment';
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import ToastContainer from '$lib/components/ToastContainer.svelte';
	import { settings } from '$lib/stores/settings.svelte.js';
	import {
		adjustHexBrightness,
		getContrastText,
		hexToRgba
	} from '$lib/utils/color.js';

	let { children } = $props();

	$effect(() => {
		if (!browser) return;
		const root = document.documentElement;
		root.setAttribute('data-theme', settings.theme);
		root.setAttribute('data-radius', settings.borderRadius);
		root.setAttribute('data-density', settings.density);

		const accent = settings.accentColor;
		const hoverDelta = settings.theme === 'dark' ? -18 : -22;
		root.style.setProperty('--accent', accent);
		root.style.setProperty('--accent-hover', adjustHexBrightness(accent, hoverDelta));
		root.style.setProperty('--accent-soft', hexToRgba(accent, settings.theme === 'dark' ? 0.15 : 0.12));
		root.style.setProperty('--accent-border', hexToRgba(accent, 0.42));
		root.style.setProperty('--accent-contrast', getContrastText(accent));
	});
</script>

<div class="app-shell">
	<Navbar />
	<main class="main-content">
		{@render children()}
	</main>
	<ToastContainer />
</div>

<style>
	.app-shell {
		min-height: 100vh;
		display: flex;
		flex-direction: column;
	}

	.main-content {
		flex: 1;
		width: 100%;
		max-width: 1360px;
		margin: 0 auto;
		padding: var(--space-lg) var(--space-md);
	}
</style>