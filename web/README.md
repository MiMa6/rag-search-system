# RAG Web Interface

A web interface for the RAG (Retrieval-Augmented Generation) system, built with Svelte and Express.js.

## Structure

- `frontend/`: Svelte + Vite + TypeScript + Tailwind CSS frontend
- `backend/`: Express.js backend that interfaces with the Python RAG system

## Prerequisites

- Node.js (v14 or later)
- Python environment with RAG dependencies installed
- ChromaDB with indexed documents

## Setup & Running

### Backend

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The backend will run on http://localhost:3000

### Frontend

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend will run on http://localhost:5173 (or another port if 5173 is in use)

## Usage

1. Make sure both frontend and backend servers are running
2. Open your browser to http://localhost:5173
3. Enter your question in the input field and click Send
4. The response will appear in the chat interface

## Development

- Frontend code is in `frontend/src/`
- Backend code is in `backend/`
- The backend uses the Python RAG system from the parent directory
