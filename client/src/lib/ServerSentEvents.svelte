<script>
  import axios from "axios";

  let message = $state("");
  let messages = $state([]);

  $effect(subscribeToMessages);

  function subscribeToMessages() {
    const eventSource = new EventSource("http://127.0.0.1:8000/sse/messages");
    eventSource.addEventListener("message", (event) => {
      const newMessages = JSON.parse(event.data);
      messages.push(...newMessages);
    });
  }

  async function sendMessage(event) {
    event.preventDefault();
    await axios.post("http://127.0.0.1:8000/sse/messages", { message }, { withCredentials: true });
    message = "";
  }
</script>

<div class="flex flex-col gap-4">
  <div class="flex flex-col gap-2 rounded border p-4 shadow">
    <h5 class="text-xl">New Message</h5>
    <form onsubmit={sendMessage} class="flex flex-col gap-4">
      <input type="text" bind:value={message} class="rounded border p-2" />
      <button type="submit" class="rounded bg-sky-700 p-2 uppercase text-white transition-colors hover:bg-sky-600">Send Message</button>
    </form>
  </div>
  <div class="flex flex-col gap-2 rounded border p-4 shadow">
    <h5 class="text-xl">Server-Sent Messages</h5>
    {#if messages.length > 0}
      <ul>
        {#each messages as message}
          <li>{message}</li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
