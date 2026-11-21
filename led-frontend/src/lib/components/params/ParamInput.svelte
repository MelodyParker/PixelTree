<script>
	import BoolParam from './BoolParam.svelte';
	import ColorParam from './ColorParam.svelte';
	import ListParam from './ListParam.svelte';
	import NumberParam from './NumberParam.svelte';

	let {
		node,
		value,
		onchange,
		linkedLengths = {},
		onResizeLinked = null,
		id = '',
		ariaLabel = '',
		depth = 0
	} = $props();
</script>

{#if node?.kind === 'number'}
	<NumberParam {value} {onchange} {id} ariaLabel={ariaLabel || 'Number'} />
{:else if node?.kind === 'bool'}
	<BoolParam {value} {onchange} {id} ariaLabel={ariaLabel || 'Boolean'} />
{:else if node?.kind === 'color'}
	<ColorParam {value} {onchange} {id} ariaLabel={ariaLabel || 'Color'} />
{:else if node?.kind === 'list'}
	<ListParam {node} {value} {onchange} {linkedLengths} {onResizeLinked} {depth} />
{:else}
	<div class="unsupported">Unsupported type: {node?.raw ?? 'unknown'}</div>
{/if}

<style>
	.unsupported {
		padding: var(--space-xs) var(--space-sm);
		border-radius: var(--radius-sm);
		border: 1px solid var(--error-border);
		background: var(--error-soft);
		color: var(--error);
		font-size: 0.9em;
	}
</style>