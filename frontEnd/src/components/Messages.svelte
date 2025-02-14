<script>
  let people = ['Alice', 'Bob', 'Charlie'];
  let selectedPerson = people[0];
  let messages = [
    { from: 'Alice', text: 'Hello!' },
    { from: 'Me', text: 'Hi, how are you?' },
  ];
  let showPeopleList = true;

  const selectPerson = (person) => {
    selectedPerson = person;
    // Load messages for the selected person
  };

  const togglePeopleList = () => {
    showPeopleList = !showPeopleList;
  };
</script>

<div class="flex h-screen">
  {#if showPeopleList}
    <div class="bg-gray-200 w-1/4 p-4">
      <button on:click={togglePeopleList} class="mb-4">Hide List</button>
      <ul>
        {#each people as person}
        <a href="?person={person}" on:click={() => selectPerson(person)}>
            <li class="cursor-pointer">
                {person}
              </li>
        </a>  
        {/each}
      </ul>
    </div>
  {/if}
  <div class="flex-1 flex flex-col">
    <div class="bg-gray-300 p-4">
      <button on:click={togglePeopleList} class="mr-4">Show List</button>
      <span>{selectedPerson}</span>
    </div>
    <div class="flex-1 p-4 overflow-y-auto">
      {#each messages as message}
        <div class="{message.from === 'Me' ? 'text-right' : 'text-left'}">
          <p><strong>{message.from}:</strong> {message.text}</p>
        </div>
      {/each}
    </div>
    <div class="p-4 bg-gray-100">
      <input type="text" placeholder="Type a message..." class="w-full p-2 border border-gray-300 rounded" />
    </div>
  </div>
</div>