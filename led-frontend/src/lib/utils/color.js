export const COLOR_PRESETS = [
	{ name: 'Red', rgb: [255, 0, 0] },
	{ name: 'Warm White', rgb: [255, 214, 170] },
	{ name: 'Gold', rgb: [255, 190, 0] },
	{ name: 'Green', rgb: [0, 220, 60] },
	{ name: 'Cyan', rgb: [0, 220, 255] },
	{ name: 'Blue', rgb: [0, 80, 255] },
	{ name: 'Purple', rgb: [160, 0, 255] },
	{ name: 'White', rgb: [255, 255, 255] },
	{ name: 'Off', rgb: [0, 0, 0] }
];

export function clampByte(val) {
	const num = Number(val);
	if (!Number.isFinite(num)) return 0;
	return Math.max(0, Math.min(255, Math.round(num)));
}

export function normalizeRgb(rgb, fallback = [255, 255, 255]) {
	if (!Array.isArray(rgb) || rgb.length !== 3) {
		return [...fallback];
	}
	return [clampByte(rgb[0]), clampByte(rgb[1]), clampByte(rgb[2])];
}

export function rgbToHex(rgb) {
	const [r, g, b] = normalizeRgb(rgb);
	return (
		'#' +
		[r, g, b]
			.map((channel) => channel.toString(16).padStart(2, '0'))
			.join('')
	);
}

export function hexToRgb(hex) {
	if (typeof hex !== 'string') return null;
	const cleaned = hex.trim().replace(/^#/, '');
	if (/^[0-9a-fA-F]{3}$/.test(cleaned)) {
		return [
			parseInt(cleaned[0] + cleaned[0], 16),
			parseInt(cleaned[1] + cleaned[1], 16),
			parseInt(cleaned[2] + cleaned[2], 16)
		];
	}
	if (/^[0-9a-fA-F]{6}$/.test(cleaned)) {
		const intVal = parseInt(cleaned, 16);
		return [(intVal >> 16) & 255, (intVal >> 8) & 255, intVal & 255];
	}
	return null;
}

export function rgbToCss(rgb) {
	const [r, g, b] = normalizeRgb(rgb);
	return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Returns dark or light foreground text hex depending on background luminance.
 */
export function getContrastText(hex) {
	const rgb = hexToRgb(hex) ?? [56, 189, 248];
	const [r, g, b] = rgb.map((c) => {
		const s = c / 255;
		return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
	});
	const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
	return luminance > 0.36 ? '#0f172a' : '#ffffff';
}

export function adjustHexBrightness(hex, delta) {
	const rgb = hexToRgb(hex) ?? [56, 189, 248];
	return rgbToHex(rgb.map((c) => clampByte(c + delta)));
}

export function hexToRgba(hex, alpha) {
	const [r, g, b] = hexToRgb(hex) ?? [56, 189, 248];
	return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}