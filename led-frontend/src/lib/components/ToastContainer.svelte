<script>
	import { toasts } from '$lib/stores/toasts.svelte.js';
</script>

{#if toasts.items.length > 0}
	<div class="toast-stack" role="region" aria-live="polite" aria-label="Notifications">
		{#each toasts.items as toast (toast.id)}
			<div class="toast {toast.type}" role="status">
				<div class="toast-body">
					<div class="toast-title">{toast.title}</div>
					{#if toast.message}
						<div class="toast-msg">{toast.message}</div>
					{/if}
				</div>
				<button
					type="button"
					class="toast-close"
					onclick={() => toasts.dismiss(toast.id)}
					aria-label="Dismiss notification"
				>
					×
				</button>
			</div>
		{/each}
	</div>
{/if}

<style>
	.toast-stack {
		position: fixed;
		right: var(--space-md);
		bottom: var(--space-md);
		z-index: 100;
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
		width: min(380px, calc(100vw - 24px));
		pointer-events: none;
	}

	.toast {
		pointer-events: auto;
		display: flex;
		align-items: flex-start;
		justify-content: space-between;
		gap: var(--space-sm);
		padding: var(--space-sm) var(--space-md);
		border-radius: var(--radius-md);
		background: var(--surface);
		border: 1px solid var(--border-strong);
		border-left-width: 4px;
		box-shadow: var(--shadow-md);
		animation: toast-in 0.18s ease-out;
	}

	.toast.success {
		border-left-color: var(--success);
	}

	.toast.error {
		border-left-color: var(--error);
	}

	.toast.info {
		border-left-color: var(--accent);
	}

	.toast-body {
		min-width: 0;
	}

	.toast-title {
		font-weight: 600;
		color: var(--text);
	}

	.toast-msg {
		margin-top: 2px;
		font-size: 0.88em;
		color: var(--text-muted);
		word-break: break-word;
	}

	.toast-close {
		background: transparent;
		border: none;
		color: var(--text-muted);
		font-size: 1.25em;
		line-height: 1;
		padding: 0 4px;
	}

	.toast-close:hover {
		color: var(--text);
	}

	@keyframes toast-in {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
</style>