**LLM Query Engine** 

A **FastAPI-powered LLM service** designed to **parse documents**, **generate embeddings**, **store and search** them in Pinecone, and **answer questions** using either a mock model or real LLMs from Hugging Face.

## 🚀 Features
- 📂 **Document ingestion** (PDF, DOCX, TXT)
- 🧠 **Semantic search** with `InstructorEmbedding` / `Sentence Transformers`
- 🗄️ **Vector storage** via Pinecone
- 🤖 **Mock or Real LLM Answering**
- 🌐 **REST API endpoint** for automated evaluation
- ⚡ **Deployable** to Railway, Render, or Ngrok

---

## 🛠 Tech Stack
- **FastAPI** – API framework
- **Pinecone** – Vector database
- **Hugging Face** – Model inference
- **Sentence Transformers** – Embedding generation
- **pdfplumber**, **python-docx** – Parsing tools
- **Uvicorn** – ASGI server

---

## 📦 Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
````

2️⃣ **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3️⃣ **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4️⃣ **Set environment variables** in `.env`:

```env
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_environment
HUGGINGFACE_API_KEY=your_huggingface_token
HUGGINGFACE_MODEL=hkunlp/instructor-xl   # or smaller model like all-MiniLM-L6-v2
```

---

## ▶️ Running Locally

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Your API will be available at:

```
http://127.0.0.1:8000
```

---

## 📡 API Usage

### **POST** `/api/v1/hackrx/run`

#### Request Body:

```json
{
  "documents": [
    "https://example.com/sample.pdf",
    "https://example.com/guide.docx"
  ],
  "query": "What is the main objective mentioned in the document?"
}
```

#### Response:

```json
{
  "answer": "The main objective is to develop a scalable AI-powered assistant.",
  "reasoning": "Matched relevant sentences containing the query keywords."
}
```

---

## 🚀 Deployment

### **Ngrok (Local Testing)**

```bash
ngrok http 8000
```

Use the generated `https://xxxxx.ngrok.io/api/v1/hackrx/run` URL for evaluation.

---

### **Railway**

1. Install the [Railway CLI](https://docs.railway.app/develop/cli)
2. Create a `Procfile`:

   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Run:

   ```bash
   railway init
   railway up
   ```
4. Set Railway environment variables (`PINECONE_API_KEY`, `HUGGINGFACE_API_KEY`, etc.).
