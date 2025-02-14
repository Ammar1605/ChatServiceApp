<script>
  let email = '';
  let password = '';

  const handleSubmit = () => {
    // Handle login logic here
    console.log('Email:', email);
    console.log('Password:', password);
  };
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
  <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <form on:submit|preventDefault={handleSubmit}>
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