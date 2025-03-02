<script>
	import { onMount, afterUpdate } from 'svelte';
	import Cookies from 'js-cookie';
	import { messages, connect, sendMessage } from '../stores/websocket.js';
  	import { writable } from 'svelte/store';

	let loading = true;
	let csrftoken = '';
	let socket;
	let messagesContainer;
	let userDetails = null;
	let people = [];
	let showPeopleList = true;
	let selectedPerson = '';
	let selectedPersonUsername = '';
	let searchQuery = '';
	let inputMessage = "";
	let inputFile = [];
	let fileSelected = false;
	let multipleFiles = false;
	let loadedMessages = 1;
	let lastScrolled = 1;
	let roomName = '';

	// Test data
	//let roomName = "testroom";
	
	onMount(async () => {
		await checkLogin();
		csrftoken = Cookies.get('csrftoken');
		await getPeopleList();
		let openedChat = new URLSearchParams(window.location.search).get('person');
		if (openedChat) {
			await selectPerson(openedChat);
			socket = connect(roomName);
			// retrieveMessages();
		}
		loading = false;
	});

	afterUpdate(() => {
		if (loadedMessages == lastScrolled) {
			scrollToBottom(); // Scroll to bottom after each update
			lastScrolled = loadedMessages;
		}
    });
	
	function scrollToBottom() {
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

	async function checkLogin() {
		const response = await fetch('http://chatservice.local/api/checkLogin', {
			method: 'GET',
			credentials: 'include', // Include cookies in the request
		});

		if (response.ok) {
			userDetails = await response.json();
		} else {
			console.log('Failed to get user details');
			window.location.href = 'http://chatservice.local/login';
		}
	}
	
	async function logout() {
		const response = await fetch('http://chatservice.local/api/logout', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			credentials: 'include',
		});
		const data = await response.json();
		if (data.status === 'OK') {
			window.location.href = 'http://chatservice.local/login';
		} else {
			alert('Failed to logout');
		}
	}

	async function getPeopleList() {
		const response = await fetch('http://chatservice.local/api/getPeopleList', {
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({'sender': userDetails.user.username})
		});
		const data = await response.json();
		if (data.status === 'OK') {
			people = data.peopleList;
		} else {
			alert('Failed to get people list');
		}
	}

	const selectPerson = async (person) => {
		let tmp = people.filter(p => p.username === person);
		selectedPerson = tmp[0].name + ' ' + tmp[0].surname;
		selectedPersonUsername = person;
		await getRoomName();
		await retrieveMessages();
		socket = connect(roomName);
		// Load messages for the selected person
	};

	async function getRoomName() {
		const response = await fetch('http://chatservice.local/api/getRoomName', {
			method: 'POST',
			credentials: 'include',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken
			},
			body: JSON.stringify({
				'sender': userDetails.user.username,
				'receiver': selectedPersonUsername
			})
		});
		const data = await response.json();
		if (data.status === 'OK') {
			roomName = data.room;
		} else {
			alert('Failed to get room name');
		}
	}

	function handleSend() {
		if (inputMessage.trim() || inputFile) {
			if ((inputFile.length > 1 && fileSelected) || inputMessage == '') {
				sendMessage(inputMessage, userDetails.user.username, selectedPersonUsername);
				for (let i = 0; i < inputFile.length; i++) {
					const reader = new FileReader();
					const filesToSend = inputFile;
                    reader.onload = () => {
                        const fileData = {
                            name: filesToSend[i].name,
                            content: reader.result.split(',')[1]
                        };
                        console.log(fileData);
                        console.log(filesToSend[i].name);
                        sendMessage(inputMessage, userDetails.user.username, selectedPersonUsername, fileData);
                    };
                    reader.readAsDataURL(filesToSend[i]);
                };
			} else if (inputFile.length == 1 && inputMessage != '') {
				const reader = new FileReader();
				const messageToSend = inputMessage;
				const filesToSend = inputFile;
				reader.onload = () => {
					const fileData = {
						name: filesToSend[0].name,
						content: reader.result.split(',')[1]
					};
					console.log(fileData);
					console.log(filesToSend[0].name);
					sendMessage(messageToSend, userDetails.user.username, selectedPersonUsername, fileData);
				};
				reader.readAsDataURL(filesToSend[0]);
				fileSelected = false;
			} else {
				sendMessage(inputMessage, userDetails.user.username, selectedPersonUsername);
			}
			for (let i = 0; i < inputFile.length; i++) {
				inputFile[i].value = '';
			}
			fileSelected = false;
			inputMessage = "";
		}
	}

	function selectFileForSend() {
		let inputElement = document.getElementById('fileInput');
		inputElement.click();
	}

	async function retrieveMessages(pageNo=null) {
		if (selectedPersonUsername != ''){
			const response = await fetch('http://chatservice.local/api/getMessages', {
				method: 'POST',
				credentials: 'include',
				headers: {
					'Content-Type': 'application/json',
					'X-CSRFToken': csrftoken
				},
				body: JSON.stringify({
					'room': roomName,
					'page': pageNo == null ? 1 : pageNo
				})
			});
			const data = await response.json();
			console.log(data);
			if (data.status != 'error') {
				messages.set(data);
			} else {
				alert('Failed to get messages');
			}
		}
	}

	function removeSelectedFile(name) {
		const filesArray = Array.from(inputFile);
		const updatedFiles = filesArray.filter(file => file.name !== name);
		if (updatedFiles.length == 0) {
			fileSelected = false;
		} else {
			const dataTransfer = new DataTransfer();
			updatedFiles.forEach(file => dataTransfer.items.add(file));
			inputFile = dataTransfer.files;
		}
	}
	
	const togglePeopleList = () => {
		showPeopleList = !showPeopleList;
	};
	
	function searchFor() {
		console.log(searchQuery);
	}
</script>

{#if loading}
	<div class="h-screen w-full flex items-center justify-center">
		<svg xmlns="http://www.w3.org/2000/svg" width="5em" height="5em" viewBox="0 0 24 24"><path fill="#221eac" d="M12 2A10 10 0 1 0 22 12A10 10 0 0 0 12 2Zm0 18a8 8 0 1 1 8-8A8 8 0 0 1 12 20Z" opacity="0.35" stroke-width="1" stroke="#221eac"/><path fill="#221eac" d="M20 12h2A10 10 0 0 0 12 2V4A8 8 0 0 1 20 12Z" stroke-width="1" stroke="#221eac"><animateTransform attributeName="transform" dur="1.75s" from="0 12 12" repeatCount="indefinite" to="360 12 12" type="rotate"/></path></svg>
	</div>
{:else}
	<div class="flex h-screen">
		<!-- People list - Left part of screen -->
		{#if showPeopleList}
			<div class="w-1/4 overflow-y-auto bg-gray-200 p-1" style="max-height: 100vh;">
				<div class="top-0 m-0 bg-gray-300 p-4">
					<h1 class="text-center">Chats</h1>
				</div>
				<div>
					<form on:submit|preventDefault={searchFor}>
						<div class="flex items-center p-2">
							<input
								type="text"
								placeholder="Search..."
								class="w-full rounded border border-gray-300 p-2"
								bind:value={searchQuery}
							>
							<button
								type="submit"
								class="cursor-pointer ml-1"
								aria-label="Search"
							>
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#2793fd" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10a7 7 0 1 0 14 0a7 7 0 1 0-14 0m18 11l-6-6"/></svg>
							</button>
						</div>
					</form>
				</div>
				<ul>
					{#each people as person}
						<li class="cursor-pointer">
							<a href="?person={person.username}" on:click={() => selectPerson(person.username)}>
								<div class="border-1 m-2 rounded-md p-2">
									{person.name} {person.surname}
								</div>
							</a>
						</li>
					{/each}
				</ul>

				<!-- My account -->
				<div class="bg-amber-500 bottom-0 left-0 m-0 w-1/4 absolute">
					<img src="favicon.png" alt="User avatar" class="w-12 h-12 rounded-full inline-block" />
					<p class="text-center inline-flex">
						{#if userDetails} 
							{userDetails.user.name} {userDetails.user.surname}
						{/if}
					</p>
					<button class="border-2 rounded-md p-1 m-1 float-right hover:cursor-pointer" on:click={logout}>
						<p class="text-center text-white hover:text-gray-400">Logout</p>
					</button>
				</div>
			</div>
		{/if}

		<!-- Messages - Right part of screen -->
		<div class="flex flex-1 flex-col">
			<!-- Header -->
			<div class="flex items-center bg-gray-300 p-4">
				<button
					on:click={togglePeopleList}
					class="mr-4 cursor-pointer"
					aria-label="Show/hide people list"
				>
					<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"
						><circle cx="9" cy="8.5" r="1.5" fill="#2793fd" opacity="0.3" /><path
							fill="#2793fd"
							d="M4.34 17h9.32c-.84-.58-2.87-1.25-4.66-1.25s-3.82.67-4.66 1.25"
							opacity="0.3"
						/><path
							fill="#2793fd"
							d="M9 12c1.93 0 3.5-1.57 3.5-3.5S10.93 5 9 5S5.5 6.57 5.5 8.5S7.07 12 9 12m0-5c.83 0 1.5.67 1.5 1.5S9.83 10 9 10s-1.5-.67-1.5-1.5S8.17 7 9 7m0 6.75c-2.34 0-7 1.17-7 3.5V19h14v-1.75c0-2.33-4.66-3.5-7-3.5M4.34 17c.84-.58 2.87-1.25 4.66-1.25s3.82.67 4.66 1.21.25s3.82.67 4.66 5zm11.7-3.19c1.16.84 1.96 1.96 1.96 3.44V19h4v-1.75c0-2.02-3.5-3.17-5.96-3.44M15 12c1.93 0 3.5-1.57 3.5-3.5S16.93 5 15 5c-.54 0-1.04.13-1.5.35c.63.89 1 1.98 1 3.15s-.37 2.26-1 3.15c.46.22.96.35 1.5.35"
						/></svg
					>
				</button>
				<span>{selectedPerson}</span>
			</div>

			<!-- Messages -->
			<div class="flex-1 overflow-y-auto p-4" bind:this={messagesContainer}>
				<!-- Load more messages -->
				<button on:click={() => {retrieveMessages(++loadedMessages)}} class="flex mx-auto p-2 rounded-xl bg-blue-500">Load more messages</button>
				
				{#each $messages as message}
					<div class='{message.sender == userDetails.user.username ? 'text-right' : 'text-left'}'>
						<span>{message.message}</span>
						{#if message.file}
							<div class='{message.sender == userDetails.user.username ? 'text-right' : 'text-left'}'>
								<a href="sharedFiles/{message.file}" download={message.file} target="_blank">
									<svg class="inline" xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><g fill="none" stroke="#5498ee" stroke-linejoin="round" stroke-width="1"><path stroke-linecap="round" d="M7 21a2 2 0 0 1-2-2V3h9l5 5v11a2 2 0 0 1-2 2z"/><path d="M13 3v6h6"/></g></svg>
									{message.file}
								</a>
							</div>
						{/if}
					</div>
				{/each}
			</div>

			<!-- Indicator for uploaded files and option for deleting some -->
			{#if fileSelected}
				<div class="bg-gray-100 p-4 block">
					{#each inputFile as iFile}
						<div class="bg-gray-200 p-2 rounded-md m-2 w-auto inline-block">
							{iFile.name}
							<button aria-label="Deselect" on:click={() => {removeSelectedFile(iFile.name)}} class="ml-2">
								<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#5498ee" d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12z"/></svg>
							</button>
						</div>
					{/each}
				</div>
			{/if}

			<!-- Input message for send -->
			<div class="bg-gray-100 p-4 flex ">
				<input
					type="text"
					placeholder="Type a message..."
					class="w-full rounded border border-gray-300 p-2 mr-1.5"
					bind:value={inputMessage}
					on:keydown={(e) => e.key === 'Enter' && handleSend()}
				/>
				<input 
					type="file" 
					class="hidden"
					bind:this={inputFile}
					on:change={(e) => {inputFile = e.target.files; fileSelected = true; multipleFiles = true; console.log(inputFile);}}
					id="fileInput"
					accept='.docx,.doc,.pdf,.txt,.png,.jpg,.jpeg,.gif,.zip,.rar,.7z,.mp4,.mkv,.mov,.webm'
					multiple
				/>
				<button aria-label="Attach File" on:click={selectFileForSend} class="hover:cursor-pointer">
					<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 20 20">
						<path fill="#5498ee" d="m4.828 10.485l5.657-5.657a3 3 0 0 1 4.243 4.243L8.01 15.788a1.5 1.5 0 0 1-2.121-2.121l6.01-6.01a.5.5 0 1 0-.707-.708l-6.01 6.01a2.5 2.5 0 0 0 3.535 3.536l6.718-6.717A4 4 0 1 0 9.778 4.12L4.12 9.778a.5.5 0 0 0 .707.707" stroke-width="0.2" stroke="#5498ee"/>
					</svg>
				</button>
				<button on:click={handleSend} class="bg-blue-500 text-white px-4 rounded ml-1.5 ">
					Send
				</button>
			</div>
		</div>
	</div>
{/if}