<script>
  import axios from "axios";

  let message = $state("");

  async function sendMessage(event) {
    event.preventDefault();
    await axios.post("http://127.0.0.1:8000/lp/messages", { message });
    message = "";
  }
</script>

<form onsubmit={sendMessage} class="flex flex-col gap-4 rounded border p-4 shadow">
  <input type="text" bind:value={message} class="rounded border p-2" />
  <button type="submit" class="rounded bg-sky-700 p-2 uppercase text-white transition-colors hover:bg-sky-600">Send Message</button>
</form>
