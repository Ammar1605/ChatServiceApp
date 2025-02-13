import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit(), tailwindcss()],
    server: {
        host: true,  // Allows access from network (0.0.0.0)
        strictPort: true,
        port: 5173,  // Change if needed
        allowedHosts: ['chatservice.local'], // Allow custom domain
    }
});
