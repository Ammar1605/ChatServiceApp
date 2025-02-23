import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
    server: {
        host: 'chatservice.local', // Use your custom domain for HMR
        strictPort: true,
        port: 5173,
        allowedHosts: ['chatservice.local'],
        hmr: {
            host: 'chatservice.local',
            protocol: 'ws',
            port: 5173,
            // Note: Vite will still append a token. There isn’t a documented way to completely remove it.
          },
    },
});
