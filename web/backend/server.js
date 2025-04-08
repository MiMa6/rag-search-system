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
    const { question, collection = "test_colection" } = req.body;
    console.log("[DEBUG] Received query:", { question, collection });

    if (!question) {
      return res.status(400).json({
        success: false,
        error: "Question is required",
      });
    }

    const options = {
      mode: "text",
      pythonPath: "python",
      scriptPath: join(__dirname, "handlers"),
      args: [question, collection],
    };

    PythonShell.run("rag_handler.py", options)
      .then((results) => {
        if (results && results.length > 0) {
          const response = JSON.parse(results[0]);
          console.log("[DEBUG] RAG response:", response);
          res.json(response);
        } else {
          console.error("[ERROR] No response from RAG handler");
          res.status(500).json({
            success: false,
            error: "No response from RAG handler",
          });
        }
      })
      .catch((err) => {
        console.error("[ERROR] RAG handler failed:", err);
        res.status(500).json({
          success: false,
          error: "Failed to process query",
        });
      });
  } catch (error) {
    console.error("[ERROR] Server error:", error);
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
