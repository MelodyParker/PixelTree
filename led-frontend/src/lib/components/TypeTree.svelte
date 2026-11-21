<script>
	import TypeTree from './TypeTree.svelte';

	let { node, depth = 0 } = $props();
</script>

<div class="tree-node" class:child={depth > 0}>
	<div class="node-line">
		{#if node?.kind === 'list'}
			{#if node.listKind === 'fixed'}
				<span class="badge mono">list_{node.length}</span>
				<span class="node-desc">Fixed-length list (exact length: {node.length})</span>
			{:else if node.listKind === 'linked'}
				<span class="badge badge-accent mono">list_{node.lengthVar}</span>
				<span class="node-desc">
					Linked list (variable length <strong class="mono">{node.lengthVar}</strong> ≥ 1, synced across params)
				</span>
			{:else}
				<span class="badge mono">list</span>
				<span class="node-desc">Dynamic list (length ≥ 1)</span>
			{/if}
		{:else if node?.kind === 'color'}
			<span class="badge badge-accent mono">color</span>
			<span class="node-desc">RGB array <span class="mono">[r, g, b]</span> (integers 0–255)</span>
		{:else if node?.kind === 'number'}
			<span class="badge mono">number</span>
			<span class="node-desc">Floating-point number</span>
		{:else if node?.kind === 'bool'}
			<span class="badge mono">bool</span>
			<span class="node-desc">Boolean (<span class="mono">true</span> / <span class="mono">false</span>)</span>
		{:else}
			<span class="badge badge-error mono">{node?.raw ?? 'unknown'}</span>
			<span class="node-desc">Unrecognized type</span>
		{/if}
	</div>

	{#if node?.kind === 'list' && node.itemType}
		<div class="children">
			<TypeTree node={node.itemType} depth={depth + 1} />
		</div>
	{/if}
</div>

<style>
	.tree-node {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.tree-node.child {
		position: relative;
		padding-left: 16px;
		margin-left: 10px;
		border-left: 2px solid var(--border-strong);
	}

	.tree-node.child::before {
		content: '';
		position: absolute;
		left: 0;
		top: 12px;
		width: 11px;
		height: 2px;
		background: var(--border-strong);
	}

	.node-line {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.node-desc {
		font-size: 0.86em;
		color: var(--text-muted);
	}

	.children {
		margin-top: 2px;
	}
</style>