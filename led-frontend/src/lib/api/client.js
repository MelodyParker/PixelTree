import { parseType } from '$lib/utils/typeParser.js';

export function normalizeBaseUrl(url) {
	return String(url ?? 'http://pi-tree:5000')
		.trim()
		.replace(/\/+$/, '');
}

function makeSlug(name, index) {
	const slug = String(name ?? '')
		.toLowerCase()
		.replace(/[^a-z0-9]+/g, '_')
		.replace(/^_|_$/g, '');
	return slug || `param_${index}`;
}

/**
 * Fetches GET /api/effects and normalizes every effect and parameter AST.
 */
export async function fetchEffects(baseUrl) {
	const root = normalizeBaseUrl(baseUrl);
	const endpoint = `${root}/api/effects`;

	let response;
	try {
		response = await fetch(endpoint, {
			method: 'GET',
			headers: { Accept: 'application/json' }
		});
	} catch (err) {
		throw new Error(
			`Could not reach ${endpoint}. Check that the server is running and CORS is enabled. (${err.message})`
		);
	}

	if (!response.ok) {
		const text = await response.text().catch(() => '');
		throw new Error(
			`Server returned HTTP ${response.status} from /api/effects${text ? `: ${text}` : ''}`
		);
	}

	const rawData = await response.json();
	if (!rawData || typeof rawData !== 'object' || Array.isArray(rawData)) {
		throw new Error('Unexpected response format from /api/effects (expected JSON object).');
	}

	const byId = {};
	const list = [];

	for (const [id, def] of Object.entries(rawData)) {
		const rawParams = Array.isArray(def?.params) ? def.params : [];
		const params = rawParams.map((param, idx) => {
			const varname = param?.varname ? String(param.varname) : makeSlug(param?.name, idx);
			const typeStr = String(param?.type ?? '');
			let ast;
			let parseError = null;
			try {
				ast = parseType(typeStr);
			} catch (err) {
				parseError = err.message;
				ast = { kind: 'number', raw: typeStr };
			}

			return {
				varname,
				name: param?.name ?? varname,
				type: typeStr,
				default: param?.default,
				ast,
				parseError
			};
		});

		const effect = {
			id,
			name: def?.name ?? id,
			description: def?.description ?? '',
			params
		};

		byId[id] = effect;
		list.push(effect);
	}

	return { byId, list };
}

/**
 * Sends POST /effect/run with native JSON parameter types.
 */
export async function runEffect(baseUrl, payload) {
	const root = normalizeBaseUrl(baseUrl);
	const endpoint = `${root}/effect/run`;

	let response;
	try {
		response = await fetch(endpoint, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Accept: 'application/json'
			},
			body: JSON.stringify(payload)
		});
	} catch (err) {
		throw new Error(
			`Network error posting to ${endpoint}. Ensure the Pi server is reachable and allows CORS POST/OPTIONS. (${err.message})`
		);
	}

	const rawText = await response.text().catch(() => '');
	let data = null;
	if (rawText) {
		try {
			data = JSON.parse(rawText);
		} catch {
			data = { raw: rawText };
		}
	}

	if (!response.ok || data?.status === 'error') {
		const msg =
			data?.error ||
			data?.message ||
			(typeof data?.raw === 'string' && data.raw) ||
			`Server returned HTTP ${response.status}`;
		throw new Error(msg);
	}

	return {
		ok: true,
		status: response.status,
		data,
		message: data?.message || `Started "${payload.id}"`
	};
}

/**
 * Utility used by Settings page to test connectivity and latency.
 */
export async function testConnection(baseUrl) {
	const start = performance.now();
	const { list } = await fetchEffects(baseUrl);
	const latencyMs = Math.round(performance.now() - start);
	return {
		count: list.length,
		latencyMs
	};
}