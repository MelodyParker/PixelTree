<script>
	import { page } from '$app/stores';
	import { effectsStore } from '$lib/stores/effects.svelte.js';
	import { settings } from '$lib/stores/settings.svelte.js';

	const navLinks = [
		{ href: '/', label: 'Runner' },
		{ href: '/effects', label: 'Effects' },
		{ href: '/settings', label: 'Settings' }
	];

	function isActive(href, pathname) {
		if (href === '/') return pathname === '/';
		return pathname === href || pathname.startsWith(`${href}/`);
	}
</script>

<header class="navbar">
	<div class="nav-inner">
		<a href="/" class="brand">
			<span class="brand-dot" aria-hidden="true"></span>
			<span class="brand-title">Pi-Tree Controller</span>
		</a>

		<nav class="nav-links" aria-label="Main navigation">
			{#each navLinks as link}
				<a
					href={link.href}
					class="nav-link"
					class:active={isActive(link.href, $page.url.pathname)}
				>
					{link.label}
				</a>
			{/each}
		</nav>

		<div class="nav-actions">
			<a href="/settings" class="status-pill" title={`Server: ${settings.apiBaseUrl}`}>
				<span
					class="status-dot"
					class:ok={effectsStore.loaded && !effectsStore.error}
					class:err={Boolean(effectsStore.error)}
					class:loading={effectsStore.loading}
				></span>
				<span class="status-text mono">
					{#if effectsStore.loading}
						Connecting…
					{:else if effectsStore.error}
						Offline
					{:else if effectsStore.loaded}
						{effectsStore.list.length} effects
					{:else}
						Idle
					{/if}
				</span>
			</a>

			<button
				type="button"
				class="btn btn-sm theme-btn"
				onclick={() => settings.toggleTheme()}
				title={`Switch to ${settings.theme === 'dark' ? 'light' : 'dark'} mode`}
				aria-label="Toggle dark and light theme"
			>
				{settings.theme === 'dark' ? '☀ Light' : '☾ Dark'}
			</button>
		</div>
	</div>
</header>

<style>
	.navbar {
		position: sticky;
		top: 0;
		z-index: 40;
		background: var(--surface);
		border-bottom: 1px solid var(--border);
		box-shadow: var(--shadow-sm);
	}

	.nav-inner {
		max-width: 1360px;
		margin: 0 auto;
		padding: var(--space-sm) var(--space-md);
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-md);
		flex-wrap: wrap;
	}

	.brand {
		display: inline-flex;
		align-items: center;
		gap: 10px;
		text-decoration: none;
		color: var(--text);
		font-weight: 700;
		font-size: 1.05em;
		letter-spacing: -0.01em;
	}

	.brand-dot {
		width: 12px;
		height: 12px;
		border-radius: 50%;
		background: var(--accent);
		box-shadow: 0 0 12px var(--accent);
	}

	.nav-links {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		padding: 4px;
		border-radius: var(--radius-md);
		background: var(--surface-subtle);
		border: 1px solid var(--border);
	}

	.nav-link {
		padding: 6px 14px;
		border-radius: var(--radius-sm);
		text-decoration: none;
		color: var(--text-muted);
		font-weight: 500;
		transition:
			background-color 0.15s ease,
			color 0.15s ease;
	}

	.nav-link:hover {
		color: var(--text);
	}

	.nav-link.active {
		background: var(--accent);
		color: var(--accent-contrast);
		font-weight: 600;
	}

	.nav-actions {
		display: inline-flex;
		align-items: center;
		gap: var(--space-xs);
	}

	.status-pill {
		display: inline-flex;
		align-items: center;
		gap: 7px;
		padding: 5px 10px;
		border-radius: 999px;
		border: 1px solid var(--border);
		background: var(--surface-elevated);
		color: var(--text-muted);
		text-decoration: none;
		font-size: 0.82em;
	}

	.status-pill:hover {
		border-color: var(--border-strong);
		color: var(--text);
	}

	.status-dot {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: var(--text-dim);
	}

	.status-dot.ok {
		background: var(--success);
		box-shadow: 0 0 8px var(--success);
	}

	.status-dot.err {
		background: var(--error);
	}

	.status-dot.loading {
		background: var(--warning);
	}

	@media (max-width: 720px) {
		.nav-inner {
			justify-content: center;
		}

		.brand {
			width: 100%;
			justify-content: center;
		}
	}
</style>