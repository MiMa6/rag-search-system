<script lang="ts">
  interface Message {
    type: "user" | "assistant";
    content: string;
  }

  let question = "";
  let response = "";
  let loading = false;
  let error = "";
  let selectedCollection = "test_colection"; // default collection
  let collections = ["test_colection", "example_collection"]; // we can fetch this later
  let messages: Message[] = [];

  async function handleSubmit() {
    if (!question.trim()) return;

    // Add user message first
    const currentQuestion = question;
    messages = [...messages, { type: "user", content: question }];
    question = ""; // Clear input after sending

    loading = true;
    error = "";

    try {
      const res = await fetch("http://localhost:3000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: currentQuestion,
          collection: selectedCollection,
        }),
      });

      const data = await res.json();

      if (data.success) {
        response = data.response;
        messages = [
          ...messages,
          {
            type: "assistant",
            content: response.replace(/^Response:\s*/i, "").trim(),
          },
        ];
      } else {
        error = data.error || "An error occurred";
        messages = [
          ...messages,
          {
            type: "assistant",
            content: `Error: ${error}`,
          },
        ];
      }
    } catch (e: any) {
      error = e.message;
      messages = [
        ...messages,
        {
          type: "assistant",
          content: `Error: ${e.message}`,
        },
      ];
    } finally {
      loading = false;
    }
  }
</script>

{#if loading}
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
  >
    <div
      class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-blue-500"
    ></div>
  </div>
{/if}

<div
  class="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12"
>
  <div class="relative py-3 sm:max-w-xl sm:mx-auto w-full px-4 sm:px-0">
    <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
      <div class="max-w-md mx-auto">
        <div class="divide-y divide-gray-200">
          <div
            class="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7"
          >
            <h2 class="text-2xl font-bold mb-8 text-center text-gray-800">
              RAG Query Interface
            </h2>

            <div class="mb-6">
              <label
                for="collection"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Select Collection
              </label>
              <select
                id="collection"
                bind:value={selectedCollection}
                class="w-full p-2 border rounded-md bg-white shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              >
                {#each collections as collection}
                  <option value={collection}>{collection}</option>
                {/each}
              </select>
            </div>

            <!-- Chat Messages -->
            <div
              class="space-y-4 mb-4 h-96 overflow-y-auto p-4 bg-gray-50 rounded-lg"
            >
              {#each messages as message}
                <div
                  class="flex flex-col {message.type === 'user'
                    ? 'items-end'
                    : 'items-start'}"
                >
                  <div
                    class="max-w-xs md:max-w-md rounded-lg px-4 py-2 {message.type ===
                    'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-800'}"
                  >
                    <p class="text-sm whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              {/each}
            </div>

            <!-- Input Form -->
            <form on:submit|preventDefault={handleSubmit} class="mt-4">
              <div class="flex space-x-3">
                <input
                  bind:value={question}
                  type="text"
                  placeholder="Ask a question..."
                  class="flex-1 form-input px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                  disabled={loading}
                />
                <button
                  type="submit"
                  class="bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50"
                  disabled={loading || !question.trim()}
                >
                  Send
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
