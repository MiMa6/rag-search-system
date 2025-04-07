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

// Helper function to run RAG query
async function runRAGQuery(question) {
  return new Promise((resolve, reject) => {
    const rootDir = join(__dirname, "../..");
    const options = {
      mode: "json", // Changed to json for structured responses
      pythonPath: "python",
      pythonOptions: ["-u"],
      scriptPath: join(__dirname, "handlers"),
      args: [question],
      cwd: rootDir,
    };

    console.log("[DEBUG] Running RAG query with options:", {
      ...options,
      workingDir: rootDir,
    });

    PythonShell.run("rag_handler.py", options)
      .then(([response]) => {
        console.log("[DEBUG] RAG response:", response);
        resolve(response);
      })
      .catch((err) => {
        console.error("[ERROR] RAG query failed:", err);
        reject(err);
      });
  });
}

app.post("/api/query", async (req, res) => {
  try {
    const { question } = req.body;
    if (!question) {
      return res.status(400).json({
        success: false,
        error: "Question is required",
      });
    }

    console.log("[DEBUG] Received question:", question);
    const response = await runRAGQuery(question);

    if (!response.success) {
      return res.status(500).json(response);
    }

    res.json(response);
  } catch (error) {
    console.error("[ERROR] Query processing failed:", error);
    res.status(500).json({
      success: false,
      error: "Internal server error",
    });
  }
});

app.get("/", (req, res) => {
  res.json({
    status: "running",
    endpoints: {
      query: "POST /api/query",
    },
  });
});

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
