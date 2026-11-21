<script>
	import { getFallbackDefault } from '$lib/utils/typeParser.js';
	import ParamInput from './ParamInput.svelte';

	let {
		node,
		value = [],
		onchange,
		linkedLengths = {},
		onResizeLinked = null,
		depth = 0
	} = $props();

	let items = $derived(Array.isArray(value) ? value : []);
	let canAddRemove = $derived(node.listKind !== 'fixed');
	let isLinked = $derived(node.listKind === 'linked');

	function handleItemChange(index, nextVal) {
		const next = [...items];
		next[index] = nextVal;
		onchange(next);
	}

	function handleAdd() {
		if (node.listKind === 'fixed') return;

		if (isLinked && onResizeLinked) {
			onResizeLinked(node.lengthVar, items.length + 1, null);
			return;
		}

		const newItem = getFallbackDefault(node.itemType, linkedLengths);
		onchange([...items, newItem]);
	}

	function handleRemove(index) {
		if (node.listKind === 'fixed' || items.length <= 1) return;

		if (isLinked && onResizeLinked) {
			onResizeLinked(node.lengthVar, items.length - 1, index);
			return;
		}

		const next = items.filter((_, i) => i !== index);
		onchange(next);
	}

	function handleMove(index, direction) {
		const target = index + direction;
		if (target < 0 || target >= items.length) return;
		const next = [...items];
		[next[index], next[target]] = [next[target], next[index]];
		onchange(next);
	}
</script>

<div class="list-param" class:nested={depth > 0}>
	<div class="list-header">
		<div class="list-meta">
			{#if node.listKind === 'fixed'}
				<span class="badge">Fixed ({node.length})</span>
			{:else if node.listKind === 'linked'}
				<span class="badge badge-accent">Linked · {node.lengthVar} = {items.length}</span>
			{:else}
				<span class="badge">List · {items.length} {items.length === 1 ? 'item' : 'items'}</span>
			{/if}
			<span class="item-type mono muted">{node.itemType.raw}</span>
		</div>

		{#if canAddRemove}
			<button type="button" class="btn btn-sm" onclick={handleAdd}>
				+ Add{isLinked ? ` (${node.lengthVar})` : ''}
			</button>
		{/if}
	</div>

	<div class="list-items">
		{#each items as item, index (index)}
			<div class="list-row">
				<div class="row-index mono">{index + 1}</div>
				<div class="row-editor">
					<ParamInput
						node={node.itemType}
						value={item}
						onchange={(nextVal) => handleItemChange(index, nextVal)}
						{linkedLengths}
						{onResizeLinked}
						depth={depth + 1}
					/>
				</div>
				<div class="row-actions">
					<button
						type="button"
						class="btn btn-ghost btn-icon"
						disabled={index === 0}
						onclick={() => handleMove(index, -1)}
						title="Move up"
						aria-label="Move item up"
					>
						↑
					</button>
					<button
						type="button"
						class="btn btn-ghost btn-icon"
						disabled={index === items.length - 1}
						onclick={() => handleMove(index, 1)}
						title="Move down"
						aria-label="Move item down"
					>
						↓
					</button>
					{#if canAddRemove}
						<button
							type="button"
							class="btn btn-ghost btn-icon remove-btn"
							disabled={items.length <= 1}
							onclick={() => handleRemove(index)}
							title={isLinked
								? `Remove index ${index + 1} from all ${node.lengthVar} lists`
								: 'Remove item'}
							aria-label="Remove item"
						>
							×
						</button>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</div>

<style>
	.list-param {
		display: flex;
		flex-direction: column;
		gap: var(--space-sm);
		padding: var(--space-sm);
		border-radius: var(--radius-md);
		border: 1px solid var(--border);
		background: var(--surface-elevated);
		width: 100%;
	}

	.list-param.nested {
		background: var(--surface);
		border-style: dashed;
	}

	.list-header {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		justify-content: space-between;
		gap: var(--space-xs);
	}

	.list-meta {
		display: flex;
		align-items: center;
		gap: var(--space-xs);
		flex-wrap: wrap;
	}

	.item-type {
		font-size: 0.82em;
	}

	.list-items {
		display: flex;
		flex-direction: column;
		gap: var(--space-xs);
	}

	.list-row {
		display: grid;
		grid-template-columns: 28px minmax(0, 1fr) auto;
		align-items: start;
		gap: var(--space-xs);
		padding: var(--space-xs);
		border-radius: var(--radius-sm);
		background: var(--surface);
		border: 1px solid var(--border);
	}

	.list-param.nested .list-row {
		background: var(--surface-elevated);
	}

	.row-index {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: var(--control-height);
		font-size: 0.82em;
		color: var(--text-dim);
		user-select: none;
	}

	.row-editor {
		min-width: 0;
	}

	.row-actions {
		display: flex;
		align-items: center;
		gap: 2px;
	}

	.remove-btn:hover:not(:disabled) {
		color: var(--error);
		border-color: var(--error-border);
		background: var(--error-soft);
	}

	@media (max-width: 560px) {
		.list-row {
			grid-template-columns: 24px minmax(0, 1fr);
		}

		.row-actions {
			grid-column: 1 / -1;
			justify-content: flex-end;
			border-top: 1px solid var(--border);
			padding-top: var(--space-xs);
		}
	}
</style>