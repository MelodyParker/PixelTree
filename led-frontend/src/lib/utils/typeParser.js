import { normalizeRgb } from './color.js';

/**
 * Safe plain-JSON deep clone (works cleanly with Svelte 5 $state proxies).
 */
export function clonePlain(value) {
	if (value === undefined) return undefined;
	return JSON.parse(JSON.stringify(value));
}

/**
 * Parses a type string into a recursive AST.
 *
 * Supported grammar:
 * - number
 * - color
 * - bool
 * - list <T>
 * - list_<num> <T>
 * - list_<letter> <T>
 */
export function parseType(typeStr) {
	const raw = String(typeStr ?? '').trim();
	if (!raw) {
		throw new Error('Empty parameter type string');
	}

	const tokens = raw.split(/\s+/);
	const head = tokens[0];
	const rest = tokens.slice(1).join(' ');

	if (head === 'number' || head === 'color' || head === 'bool') {
		if (rest) {
			throw new Error(`Unexpected trailing tokens after "${head}" in "${raw}"`);
		}
		return { kind: head, raw };
	}

	if (head === 'list') {
		if (!rest) {
			throw new Error(`Missing item type in "${raw}"`);
		}
		return {
			kind: 'list',
			listKind: 'dynamic',
			itemType: parseType(rest),
			raw
		};
	}

	const fixedMatch = /^list_(\d+)$/.exec(head);
	if (fixedMatch) {
		const length = Number.parseInt(fixedMatch[1], 10);
		if (!Number.isInteger(length) || length < 1) {
			throw new Error(`Fixed list length must be >= 1 in "${raw}"`);
		}
		if (!rest) {
			throw new Error(`Missing item type in "${raw}"`);
		}
		return {
			kind: 'list',
			listKind: 'fixed',
			length,
			itemType: parseType(rest),
			raw
		};
	}

	const linkedMatch = /^list_([A-Za-z][A-Za-z0-9]*)$/.exec(head);
	if (linkedMatch) {
		if (!rest) {
			throw new Error(`Missing item type in "${raw}"`);
		}
		return {
			kind: 'list',
			listKind: 'linked',
			lengthVar: linkedMatch[1],
			itemType: parseType(rest),
			raw
		};
	}

	throw new Error(`Unsupported parameter type "${raw}"`);
}

/**
 * Collects all linked length variable names (e.g., "N") present anywhere in an AST.
 */
export function collectLinkedVars(node, targetSet = new Set()) {
	if (!node) return targetSet;
	if (node.kind === 'list') {
		if (node.listKind === 'linked') {
			targetSet.add(node.lengthVar);
		}
		collectLinkedVars(node.itemType, targetSet);
	}
	return targetSet;
}

/**
 * Generates a fresh fallback default value for any AST node.
 */
export function getFallbackDefault(node, linkedLengths = {}) {
	switch (node.kind) {
		case 'number':
			return 1;
		case 'color':
			return [255, 255, 255];
		case 'bool':
			return false;
		case 'list': {
			let count = 1;
			if (node.listKind === 'fixed') {
				count = node.length;
			} else if (node.listKind === 'linked') {
				count = Math.max(1, Number(linkedLengths[node.lengthVar]) || 1);
			}
			return Array.from({ length: count }, () =>
				getFallbackDefault(node.itemType, linkedLengths)
			);
		}
		default:
			return null;
	}
}

/**
 * Parses a raw default value from `/api/effects` (which may be a JSON-encoded string
 * or already native JSON) without throwing.
 */
function decodeRawDefault(rawDefault) {
	if (rawDefault === undefined || rawDefault === null || rawDefault === '') {
		return { hasValue: false, parsed: undefined };
	}

	if (typeof rawDefault !== 'string') {
		return { hasValue: true, parsed: rawDefault };
	}

	const trimmed = rawDefault.trim();
	if (trimmed === '') {
		return { hasValue: false, parsed: undefined };
	}

	// Tolerate Python-style booleans ("True"/"False") as well as standard JSON
	if (/^true$/i.test(trimmed)) return { hasValue: true, parsed: true };
	if (/^false$/i.test(trimmed)) return { hasValue: true, parsed: false };

	try {
		return { hasValue: true, parsed: JSON.parse(trimmed) };
	} catch {
		const asNumber = Number(trimmed);
		if (Number.isFinite(asNumber)) {
			return { hasValue: true, parsed: asNumber };
		}
		return { hasValue: false, parsed: undefined };
	}
}

/**
 * Extracts linked list lengths from a candidate value matching the AST.
 */
export function inferLinkedLengths(node, value, lengths = {}) {
	if (!node || node.kind !== 'list' || !Array.isArray(value)) {
		return lengths;
	}

	if (node.listKind === 'linked' && value.length >= 1) {
		const existing = lengths[node.lengthVar] || 0;
		lengths[node.lengthVar] = Math.max(existing, value.length);
	}

	for (const item of value) {
		inferLinkedLengths(node.itemType, item, lengths);
	}

	return lengths;
}

/**
 * Validates and coerces any value to strictly match the AST and current linked lengths.
 */
export function coerceValue(node, value, linkedLengths = {}) {
	switch (node.kind) {
		case 'number': {
			const num = Number(value);
			return Number.isFinite(num) ? num : 1;
		}
		case 'bool': {
			if (typeof value === 'boolean') return value;
			if (typeof value === 'string') return value.trim().toLowerCase() === 'true';
			return Boolean(value);
		}
		case 'color': {
			return normalizeRgb(value, [255, 255, 255]);
		}
		case 'list': {
			const arr = Array.isArray(value) ? value : [];
			let targetLen;

			if (node.listKind === 'fixed') {
				targetLen = node.length;
			} else if (node.listKind === 'linked') {
				targetLen = Math.max(1, Number(linkedLengths[node.lengthVar]) || arr.length || 1);
			} else {
				targetLen = Math.max(1, arr.length);
			}

			const result = [];
			for (let i = 0; i < targetLen; i++) {
				if (i < arr.length) {
					result.push(coerceValue(node.itemType, arr[i], linkedLengths));
				} else {
					result.push(getFallbackDefault(node.itemType, linkedLengths));
				}
			}
			return result;
		}
		default:
			return value;
	}
}

/**
 * Parses a single parameter's default value and indicates whether the server supplied one.
 */
export function parseDefaultValue(node, rawDefault, linkedLengths = {}) {
	const { hasValue, parsed } = decodeRawDefault(rawDefault);
	if (!hasValue) {
		return {
			value: getFallbackDefault(node, linkedLengths),
			usedServerDefault: false
		};
	}
	return {
		value: coerceValue(node, parsed, linkedLengths),
		usedServerDefault: true
	};
}

/**
 * Recursively resizes every `list_<targetVar>` inside `value` to `newLength`.
 * If `removeIndex` is provided and shrinking by 1, that specific index is removed in lockstep.
 */
export function resizeLinkedListsInValue(
	node,
	value,
	targetVar,
	newLength,
	linkedLengths = {},
	removeIndex = null
) {
	if (!node || node.kind !== 'list') {
		return value;
	}

	const currentArr = Array.isArray(value) ? [...value] : [];
	let workingArr = currentArr;

	if (node.listKind === 'linked' && node.lengthVar === targetVar) {
		const clampedLen = Math.max(1, Math.floor(newLength));
		if (
			removeIndex !== null &&
			removeIndex >= 0 &&
			removeIndex < workingArr.length &&
			workingArr.length - 1 === clampedLen
		) {
			workingArr.splice(removeIndex, 1);
		} else if (workingArr.length > clampedLen) {
			workingArr = workingArr.slice(0, clampedLen);
		} else {
			while (workingArr.length < clampedLen) {
				workingArr.push(getFallbackDefault(node.itemType, linkedLengths));
			}
		}
	}

	return workingArr.map((item) =>
		resizeLinkedListsInValue(
			node.itemType,
			item,
			targetVar,
			newLength,
			linkedLengths,
			removeIndex
		)
	);
}

/**
 * Builds synchronized initial parameter values and linked length map for an effect.
 * Optionally accepts an override `seedValues` map (e.g., when loading from History).
 */
export function buildInitialEffectState(effect, seedValues = null) {
	const params = effect?.params ?? [];
	const linkedVarSet = new Set();
	const linkedLengths = {};

	// 1. Discover all linked length variables across all parameters
	for (const param of params) {
		collectLinkedVars(param.ast, linkedVarSet);
	}
	for (const v of linkedVarSet) {
		linkedLengths[v] = 1;
	}

	// 2. First pass: decode seed values or server defaults and infer shared linked lengths
	const decodedMap = {};
	for (const param of params) {
		if (seedValues && Object.prototype.hasOwnProperty.call(seedValues, param.varname)) {
			const seeded = clonePlain(seedValues[param.varname]);
			decodedMap[param.varname] = { hasValue: true, parsed: seeded };
			inferLinkedLengths(param.ast, seeded, linkedLengths);
		} else {
			const decoded = decodeRawDefault(param.default);
			decodedMap[param.varname] = decoded;
			if (decoded.hasValue) {
				inferLinkedLengths(param.ast, decoded.parsed, linkedLengths);
			}
		}
	}

	// 3. Second pass: coerce every parameter using the final synchronized linked lengths
	const values = {};
	for (const param of params) {
		const entry = decodedMap[param.varname];
		if (entry?.hasValue) {
			values[param.varname] = coerceValue(param.ast, entry.parsed, linkedLengths);
		} else {
			values[param.varname] = getFallbackDefault(param.ast, linkedLengths);
		}
	}

	return {
		values,
		linkedLengths,
		linkedVars: Array.from(linkedVarSet)
	};
}

/**
 * Checks if a plain value looks like an [R, G, B] tuple (useful when displaying history).
 */
export function isRgbTuple(val) {
	return (
		Array.isArray(val) &&
		val.length === 3 &&
		val.every((n) => typeof n === 'number' && Number.isFinite(n) && n >= 0 && n <= 255)
	);
}

/**
 * Produces a concise human-readable description of a type AST node.
 */
export function describeType(node) {
	if (!node) return 'Unknown type';
	switch (node.kind) {
		case 'number':
			return 'Floating-point number';
		case 'color':
			return 'RGB color [R, G, B] (0–255)';
		case 'bool':
			return 'Boolean (true / false)';
		case 'list': {
			const inner = describeType(node.itemType);
			if (node.listKind === 'fixed') {
				return `Fixed list of exactly ${node.length} × (${inner})`;
			}
			if (node.listKind === 'linked') {
				return `Linked list of length ${node.lengthVar} (≥ 1) × (${inner})`;
			}
			return `Dynamic list (≥ 1) of (${inner})`;
		}
		default:
			return node.raw ?? 'Unknown';
	}
}