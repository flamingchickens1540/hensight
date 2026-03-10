import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	ssr: {
		external: ['bun:sqlite']
	},
	server: {
		allowedHosts: ['furless-devona-proequality.ngrok-free.dev']
	}
});
