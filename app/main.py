import os, json, logging, hashlib
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from .models import RunRequest, RunResponse, AnswerItem, SourcePassage
from .utils import download_file, compute_doc_hash, chunk_text
from .parser import extract_text_from_pdf, extract_text_from_docx
from .embedder import EmbeddingModel
from .retriever import InMemoryRetriever
from .llm_engine import generate_answer

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title='HackRx LLM Query-Retrieval (Mock-ready)')

TEAM_TOKEN = os.getenv('TEAM_TOKEN', 'ac754e4d756d022ff347e41720a4091d60b8cf2e0a41a797a94da49b56491ce9')
USE_MOCK = os.getenv('USE_MOCK', 'true').lower() in ('1','true','yes')

@app.post('/api/v1/hackrx/run', response_model=RunResponse)
async def run_query(request: RunRequest, authorization: str = Header(None)):
    # Authorization check (simple Bearer token match)
    if not authorization:
        raise HTTPException(status_code=422, detail='Authorization header required')
    if not authorization.lower().startswith('bearer '):
        raise HTTPException(status_code=401, detail='Bearer token required')
    token = authorization.split(' ',1)[1].strip()
    if token != TEAM_TOKEN:
        raise HTTPException(status_code=401, detail='Invalid team token')

    # Document handling
    doc_url = request.documents
    logger.info('Received request for document: %s', doc_url)
    try:
        local_path = download_file(doc_url)
    except Exception as e:
        logger.error('Failed downloading doc: %s', e)
        raise HTTPException(status_code=400, detail='Unable to download document')

    # Extract text (PDF/DOCX)
    suffix = local_path.split('.')[-1].lower()
    if suffix in ['pdf']:
        pages = extract_text_from_pdf(local_path)
    elif suffix in ['docx']:
        pages = extract_text_from_docx(local_path)
    else:
        # fallback: try PDF parser
        pages = extract_text_from_pdf(local_path)

    # chunk pages into passages
    passages = []
    for page_num, txt in pages:
        for chunk in chunk_text(txt, chunk_size=200, overlap=40):
            passages.append({'text': chunk, 'page': page_num})

    texts = [p['text'] for p in passages]
    if not texts:
        raise HTTPException(status_code=422, detail='No text extracted from document')

    # Embedding 
    embedder = EmbeddingModel()
    embeddings = embedder.fit_transform(texts)  # N x D

    # Retriever
    retriever = InMemoryRetriever(embeddings, passages)
    answers = []

    for q in request.questions:
        q_emb = embedder.transform([q])[0]  # D
        hits = retriever.query(q_emb, top_k=5)
        # hits: list of tuples (meta,text,score)
        # Feed to LLM (mock/generic)
        result = generate_answer(q, hits)
        sources = []
        for meta, text, score in hits:
            sources.append(SourcePassage(text=text, page=meta.get('page'), score=score))
        answers.append(AnswerItem(answer=result['answer'], sources=sources, reasoning=result.get('reasoning')))

    # cleanup temp file
    try:
        os.remove(local_path)
    except Exception:
        pass

    return RunResponse(answers=answers)
