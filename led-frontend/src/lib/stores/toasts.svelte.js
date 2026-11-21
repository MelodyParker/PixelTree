let nextToastId = 1;

class ToastStore {
	items = $state([]);

	add({ type = 'info', title = '', message = '', duration = 4000 }) {
		const id = nextToastId++;
		this.items = [...this.items, { id, type, title, message }];

		if (duration > 0) {
			setTimeout(() => {
				this.dismiss(id);
			}, duration);
		}
		return id;
	}

	success(title, message = '', duration = 3500) {
		return this.add({ type: 'success', title, message, duration });
	}

	error(title, message = '', duration = 6000) {
		return this.add({ type: 'error', title, message, duration });
	}

	info(title, message = '', duration = 3500) {
		return this.add({ type: 'info', title, message, duration });
	}

	dismiss(id) {
		this.items = this.items.filter((t) => t.id !== id);
	}
}

export const toasts = new ToastStore();