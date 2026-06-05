# rag.py
# Handles PDF ingestion and per-thread retriever management for the RAG pipeline.
#
# How it works:
#   1. ingest_pdf()   — receives raw PDF bytes, splits into chunks via pypdf,
#                        embeds them with Azure OpenAI, stores in a FAISS index,
#                        and caches the resulting retriever keyed by thread_id.
#   2. get_retriever() — returns the cached FAISS retriever for a given thread.
#   3. sync_from_session() — called at the start of every Streamlit re-run to
#                        restore module-level caches from st.session_state
#                        (Streamlit resets module globals on each re-run).

from __future__ import annotations

import os
import tempfile
from typing import Any, Dict, Optional

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import embeddings

# Module-level dicts keyed by thread_id.
# These are the source of truth during a single Streamlit run;
# session_state is used only to survive re-runs.
_thread_retrievers: Dict[str, Any] = {}
_thread_metadata: Dict[str, dict] = {}


def get_retriever(thread_id: Optional[str]):
    if thread_id and thread_id in _thread_retrievers:
        return _thread_retrievers[thread_id]
    return None


def get_metadata(thread_id: Optional[str]) -> dict:
    return _thread_metadata.get(str(thread_id), {}) if thread_id else {}


def ingest_pdf(file_bytes: bytes, thread_id: str, filename: Optional[str] = None) -> dict:
    if not file_bytes:
        raise ValueError("No bytes received for ingestion.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name

    try:
        docs = PyPDFLoader(temp_path).load()
        chunks = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
        ).split_documents(docs)

        retriever = FAISS.from_documents(chunks, embeddings).as_retriever(
            search_type="similarity", search_kwargs={"k": 5}
        )

        _thread_retrievers[thread_id] = retriever
        meta = {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }
        _thread_metadata[thread_id] = meta

        # Persist to session_state so retrievers survive Streamlit re-runs
        st.session_state.setdefault("_thread_retrievers", {})[thread_id] = retriever
        st.session_state.setdefault("_thread_metadata", {})[thread_id] = meta
        return meta
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def sync_from_session():
    """Restore retrievers and metadata from session_state after a Streamlit re-run."""
    _thread_retrievers.update(st.session_state.get("_thread_retrievers", {}))
    _thread_metadata.update(st.session_state.get("_thread_metadata", {}))
