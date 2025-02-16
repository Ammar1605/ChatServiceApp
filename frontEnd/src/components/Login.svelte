<script>
  import { onMount } from 'svelte';
  import Cookies from 'js-cookie';

  let email = '';
  let password = '';
  let csrftoken = '';

  onMount(async () => {
    if (!Cookies.get('csrftoken')) {
      await getCSRFToken();
    }
    csrftoken = Cookies.get('csrftoken');
  });

  async function getCSRFToken() {
      const response = await fetch('api/getcsrf', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();
    }

  async function handleLogin() {
    const response = await fetch('http://chatservice.local/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    if (result.status == 'OK') {
      console.log('Login successful');
      window.location.href = 'http://chatservice.local/messages';
    } else if (result.status_code == 401) {
      console.log('Login failed - invalid credentials');
    } else {
      console.log('Login failed - unknown error');
    }
    /* event.preventDefault();
		loginData.email = email;
		loginData.password = CryptoJS.SHA256(password).toString();

		loginData.sessionID = localStorage.getItem('sessionid');

		try {
			const response = await fetch('api/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken
				},
				body: JSON.stringify(loginData)
			});

			const result = await response.json();

			if (result.status == 'prijavljen') {
				let uporabnik = {
					username: result.username,
					brezplacnoPolnjenje: result.brezplacnoPolnjenje,
					role: result.role,
					podjetje: result.podjetje,
          			enaslov: loginData.enaslov
				};
				logged = true;
				loggingIn(uporabnik);
			} else if (result.status == 'Prijavljen drugje') {
				alert('Napaka! Ste že prijavljeni na drugi napravi ali drugem brskalniku');
			} else if (result.status == 'Napaka') {
				alert('Napaka!! Sporočilo: ', result.podatki, ' Boste preusmerjeni nazaj.');
				window.location.href = 'http://xpandlink.com/charger?chargerID=' + stringify(chargerID);
			} else {
				logged = false;
				alert(result.status);
			}
		} catch (error) {
			console.log(error);
		} */
  };
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form on:submit|preventDefault={handleLogin}>
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
        <input type="email" id="email" bind:value={email} class="w-full p-2 border border-gray-300 rounded mt-2" required />
      </div>
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <input type="password" id="password" bind:value={password} class="w-full p-2 border border-gray-300 rounded mt-2" required />
      </div>
      <button type="submit" class="w-full bg-blue-500 text-white p-2 rounded mt-4">Login</button>
    </form>
  </div>
</div>