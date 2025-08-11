import os
import requests
from typing import List, Dict, Any

HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN', None)
OPENAI_KEY = os.getenv('OPENAI_API_KEY', None)
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', None)  # e.g., mistral, llama3, gemma2

def query_ollama(prompt: str) -> str:
    """
    Send a prompt to a locally running Ollama model and return the generated text.
    Ollama must be running locally: `ollama serve`
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": OLLAMA_MODEL or "mistral",
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"[Ollama Error] {e}"

def generate_answer_mock(query: str, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
    q_tokens = set([t.lower() for t in query.split() if len(t) > 3])
    found = []
    for meta, text, score in passages:
        sents = [s.strip() for s in text.split('.') if s.strip()]
        for s in sents:
            low = s.lower()
            if any(tok in low for tok in q_tokens):
                found.append((s, meta.get('page'), score))
    if found:
        answer = ' '.join([f"{s.strip()}" for s, p, sc in found[:3]])
        reasoning = f"Matched {len(found)} sentence(s) using keyword heuristics."
    else:
        conc = ' '.join([p[0].get('text', '') for p in passages[:3]])
        answer = conc[:1200] + ('...' if len(conc) > 1200 else '')
        reasoning = 'No direct sentence match; returning top passages concatenation.'
    return {'answer': answer, 'reasoning': reasoning}

def generate_answer(query: str, passages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generates an answer using Ollama if available, otherwise falls back to mock method.
    """
    if OLLAMA_MODEL:
        # Build a prompt using the retrieved passages
        context_text = "\n\n".join([f"[Page {meta.get('page', '?')}] {text}" for meta, text, score in passages])
        prompt = (
            f"You are a helpful assistant. Answer the following query based only on the provided context.\n\n"
            f"Query: {query}\n\n"
            f"Context:\n{context_text}\n\n"
            f"Answer:"
        )
        answer = query_ollama(prompt)
        reasoning = f"Answer generated using Ollama model '{OLLAMA_MODEL or 'mistral'}'."
        return {'answer': answer, 'reasoning': reasoning}

    elif HUGGINGFACE_TOKEN or OPENAI_KEY:
        # TODO: Integrate with HF inference or OpenAI if needed
        pass

    # Default to mock if no LLM integration
    return generate_answer_mock(query, passages)
