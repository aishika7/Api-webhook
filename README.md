# Final_LLM (HackRx) — Delivery bundle (Mock + Real-ready)

This repository is a **deployable, reviewable** backend for the HackRx LLM Query-Retrieval task.
It contains a working **mock model** (fast, local) and hooks to replace the mock with **real embeddings/LLMs** (Hugging Face / Pinecone / OpenAI) later.

**Contents**
- `app/` — FastAPI app and modules (parser, embedder, retriever, llm_engine, utils)
- `requirements.txt` — minimal dependencies for local/mocked testing
- `runtime.txt` — force Python 3.10 on Render
- `render.yaml` — sample Render configuration (adjust secrets in Render UI)
- `.env.template` — environment variable template (DO NOT COMMIT real secrets)

**Quick start (local)**
1. Create venv and activate
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\\Scripts\\activate
   ```
2. Install requirements
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Create .env from `.env.template` and fill keys (or set env vars)
4. Run the app
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. Open Swagger: http://127.0.0.1:8000/docs
6. Test with Postman (see README "Postman testing" section).

**Notes**
- The default behavior uses a **mock TF-IDF based "embedding"** (fast) that works offline and produces explainable retrievals. Set `USE_MOCK=true` (default).
- To use real embeddings and vector DB:
  - Provide `PINECONE_API_KEY` + `PINECONE_ENV` (the code will use Pinecone if present).
  - Install heavy ML libs (sentence-transformers / InstructorEmbedding) if you want local S-BERT embeddings.
  - Provide `HUGGINGFACEHUB_API_TOKEN` or `OPENAI_API_KEY` to enable actual LLM generation.
