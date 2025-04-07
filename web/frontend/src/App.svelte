<script lang="ts">
  interface Message {
    type: "user" | "assistant";
    content: string;
  }

  let question: string = "";
  let messages: Message[] = [];
  let loading: boolean = false;

  async function handleSubmit() {
    if (!question.trim() || loading) return;

    // Add user message
    messages = [...messages, { type: "user", content: question }];
    const currentQuestion = question;
    question = "";
    loading = true;

    try {
      const response = await fetch("http://localhost:3000/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: currentQuestion }),
      });

      const data = await response.json();

      // Add assistant message with the cleaned response
      messages = [
        ...messages,
        {
          type: "assistant",
          content: data.response.replace(/^Response:\s*/i, "").trim(),
        },
      ];
    } catch (error) {
      console.error("Error:", error);
      messages = [
        ...messages,
        {
          type: "assistant",
          content: "Sorry, there was an error processing your request.",
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
