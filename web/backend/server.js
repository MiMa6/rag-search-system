import express from "express";
import cors from "cors";
import { PythonShell } from "python-shell";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

// Root route
app.get("/", (req, res) => {
  res.json({
    status: "RAG API Server is running",
    endpoints: {
      query: "POST /api/query",
    },
  });
});

// Helper function to run Python script
function runPythonScript(question) {
  return new Promise((resolve, reject) => {
    const rootDir = join(__dirname, "../../");
    console.log(`[DEBUG] Running query with question: "${question}"`);
    console.log(`[DEBUG] Working directory: ${rootDir}`);

    const options = {
      mode: "text",
      pythonPath: join(rootDir, ".venv/bin/python"),
      pythonOptions: ["-u"], // unbuffered output
      scriptPath: rootDir,
      args: ["--question", question, "--collection-name", "test_docs_eng_2"],
      cwd: rootDir, // Set the working directory to the project root
    };

    console.log(`[DEBUG] Python script options:`, options);

    PythonShell.run("example_query.py", options)
      .then((messages) => {
        console.log(`[DEBUG] Raw Python output:`, messages);

        // Process the output to extract just the response
        const fullResponse = messages.join("\n");
        console.log(`[DEBUG] Full response:`, fullResponse);

        // Look for the actual response after "Response:" in the output
        const responseMatch = fullResponse.match(
          /Response:\n([\s\S]*?)(?=\n\n|$)/
        );
        if (responseMatch && responseMatch[1]) {
          const cleanResponse = responseMatch[1].trim();
          console.log(`[DEBUG] Cleaned response:`, cleanResponse);
          resolve(cleanResponse);
        } else {
          console.log(`[DEBUG] No response match found, returning full output`);
          resolve(fullResponse);
        }
      })
      .catch((err) => {
        console.error("[ERROR] Error running Python script:", err);
        reject(err);
      });
  });
}

app.post("/api/query", async (req, res) => {
  try {
    console.log("\n[DEBUG] Received query request:", req.body);
    const { question } = req.body;
    if (!question) {
      console.log("[ERROR] No question provided in request");
      return res.status(400).json({ error: "Question is required" });
    }

    const response = await runPythonScript(question);
    console.log("[DEBUG] Sending response:", response);
    res.json({ response });
  } catch (error) {
    console.error("[ERROR] Error processing query:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
