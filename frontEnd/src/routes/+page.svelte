<script>
    import { onMount } from 'svelte';
    import Cookies from 'js-cookie';

    let loggedIn = false;

    onMount(async () => {
        await checkLogin();
        if (loggedIn) {
            window.location.href = 'http://chatservice.local/messages';
        } else {
            window.location.href = 'http://chatservice.local/login';
        } 
    });
    
    async function checkLogin() {
		const response = await fetch('http://chatservice.local/api/checkLogin', {
			method: 'GET',
			credentials: 'include', // Include cookies in the request
		});

		if (response.ok) {
			loggedIn = true;
		} else {
			console.log('Failed to get user details');
		}
	}
</script>

<div class="h-screen w-full flex items-center justify-center">
    <svg xmlns="http://www.w3.org/2000/svg" width="5em" height="5em" viewBox="0 0 24 24"><path fill="#221eac" d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8A8 8 0 0 1 12 20Z" opacity="0.35" stroke-width="1" stroke="#221eac"/><path fill="#221eac" d="M20 12h2A10 10 0 0 0 12 2V4A8 8 0 0 1 20 12Z" stroke-width="1" stroke="#221eac"><animateTransform attributeName="transform" dur="1.75s" from="0 12 12" repeatCount="indefinite" to="360 12 12" type="rotate"/></path></svg>
</div>