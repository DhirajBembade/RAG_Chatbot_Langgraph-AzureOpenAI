# PDF Extraction Libraries for RAG Pipelines

## The Core Challenge

- Regular PDF parsers only extract **embedded text layers**
- Images, diagrams, and architecture charts have text **baked into pixels**
- For those, you need **OCR** or a **multimodal LLM**
- No parser truly *understands* diagrams — they only OCR the visible labels

---

## Library Comparison

### 1. Docling (by IBM) — Recommended for RAG

**Install:**
```bash
pip install docling
```

**Why use it:**
- Extracts text, tables (as structured data), and runs OCR on embedded images
- Outputs clean Markdown and JSON — ideal for chunking and vector stores
- Handles scanned PDFs, multi-column layouts, and complex formatting
- Completely free and open source
- Native LangChain / LlamaIndex compatibility

**Best for:** General-purpose RAG pipelines, structured document understanding

---

### 2. Unstructured — Best for Messy or Complex PDFs

**Install:**
```bash
pip install unstructured[pdf]
```

**Why use it:**
- Uses Tesseract OCR under the hood for image text
- Classifies every element: Title, Table, Image, NarrativeText, ListItem, etc.
- Handles scanned PDFs, mixed-format documents
- Widely used in production RAG systems
- Integrates directly with LangChain via `UnstructuredPDFLoader`

**Best for:** Documents with inconsistent formatting or heavy image content

---

### 3. Azure Document Intelligence — Best for Azure-based Projects

**Install:**
```bash
pip install azure-ai-documentintelligence
```

**Why use it:**
- Cloud API with very high accuracy for tables, forms, handwriting, and diagrams
- Integrates directly with LangChain via `AzureAIDocumentIntelligenceLoader`
- Since this project already uses Azure OpenAI, it fits naturally into the stack
- Handles architecture diagrams by OCR-ing all visible text labels
- Supports many document types: invoices, contracts, technical docs

**Best for:** Projects already on Azure, high-accuracy enterprise document processing

---

### 4. pymupdf4llm — Best for Clean Text + Tables

**Install:**
```bash
pip install pymupdf4llm
```

**Why use it:**
- Official library by Artifex (PyMuPDF makers), built for LLM use cases
- Converts PDF pages to clean Markdown — preserves headings, tables, lists
- Better table extraction than plain PyPDFLoader
- Per-page chunking with metadata (page number, source)
- Replaces the deprecated `PyMuPDFLoader` from `langchain-community`

**Limitation:** No OCR — cannot extract text from images or diagrams

**Best for:** Text-heavy PDFs with clean embedded text and structured tables

---

### 5. marker-pdf — Best Text/Table Accuracy

**Install:**
```bash
pip install marker-pdf
```

**Why use it:**
- Very high fidelity Markdown conversion from PDFs
- Excellent at preserving document structure and table formatting
- Faster than Docling for simple documents

**Limitation:** Limited support for diagram or image text extraction

**Best for:** Academic papers, reports, and well-structured documents

---

## Handling Diagram and Architecture Text

- OCR tools extract visible **text labels** from diagrams (box names, arrows, annotations)
- They do NOT understand the meaning or relationships in the diagram
- For true diagram understanding, pass the image to a **multimodal LLM**

**Example approach:**
```python
# Step 1: Extract diagram as image using Docling or pymupdf4llm
# Step 2: Send image to GPT-4o on Azure for understanding

from openai import AzureOpenAI
import base64

with open("diagram.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")

client = AzureOpenAI(...)
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
                {"type": "text", "text": "Describe all components and relationships shown in this diagram."}
            ]
        }
    ]
)
```

---

## Summary Table

| Library              | Text | Tables | Image OCR | Diagram Understanding | License  | Cost  |
|----------------------|------|--------|-----------|----------------------|----------|-------|
| Docling              | Yes  | Yes    | Yes       | Labels only (OCR)    | MIT      | Free  |
| Unstructured         | Yes  | Yes    | Yes       | Labels only (OCR)    | Apache   | Free  |
| Azure Doc Intelligence | Yes | Yes  | Yes       | Labels only (OCR)    | Proprietary | Paid |
| pymupdf4llm          | Yes  | Yes    | No        | No                   | AGPL     | Free  |
| marker-pdf           | Yes  | Yes    | No        | No                   | GPL      | Free  |
| GPT-4o Vision        | Yes  | Yes    | Yes       | Yes (full meaning)   | Proprietary | Paid |

---

## Recommended Stack for This Project

Since this project uses **Azure OpenAI**:

```
Docling  →  Extract text, tables, image OCR
    +
Azure OpenAI GPT-4o  →  Understand diagrams and architecture images
    +
LangChain RAG Pipeline  →  Chunk, embed, retrieve, answer
```

- Use **Docling** as the primary extractor for all PDF content
- Use **Azure Document Intelligence** if higher accuracy is needed on complex documents
- Use **GPT-4o multimodal** for any diagram or architecture image that needs semantic understanding
