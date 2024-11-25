<script>
  import "./app.css";
  import LongPolling from "./lib/LongPolling.svelte";
  import ServerSentEvents from "./lib/ServerSentEvents.svelte";

  let view = $state("lp");

  function changeView(newView) {
    view = newView;
  }
</script>

<main class="container mx-auto flex flex-col gap-4 p-4">
  <div class="flex justify-center gap-4">
    {#if view === "lp"}
      <button class="rounded border bg-sky-700 p-2 text-white hover:bg-sky-600">Long Polling</button>
    {:else}
      <button type="button" onclick={() => changeView("lp")} class="rounded border p-2 transition-colors hover:bg-sky-600 hover:text-white">
        Long Polling
      </button>
    {/if}
    {#if view === "sse"}
      <button class="rounded border bg-sky-700 p-2 text-white hover:bg-sky-600">Server-Sent Events</button>
    {:else}
      <button type="button" onclick={() => changeView("sse")} class="rounded border p-2 transition-colors hover:bg-sky-600 hover:text-white">
        Server-Sent Events
      </button>
    {/if}
  </div>
  <div>
    {#if view === "lp"}
      <LongPolling />
    {:else if view === "sse"}
      <ServerSentEvents />
    {/if}
  </div>
</main>
