# LLM Token Limits, Context Windows & API Rate Limits

> Last updated: June 2026. Limits change frequently — always verify with official provider docs.

---

## What is a Token?

- 1 token ≈ 4 characters or 0.75 words in English
- "Hello world" = 2 tokens
- 1,000 tokens ≈ 750 words ≈ ~1.5 pages of text
- Images, PDFs, and audio also consume tokens when passed to multimodal models

---

## 1. Anthropic Claude Models (Latest 2026)

| Model | Context Window | Max Output | Best Use Case |
|---|---|---|---|
| **Claude Opus 4.8** | 1M tokens | 32K tokens (300K via beta) | Most powerful — complex reasoning, long-horizon agentic coding, high-autonomy enterprise |
| **Claude Opus 4.7** | 1M tokens | 32K tokens (300K via beta) | High capability reasoning, research, autonomous agents |
| Claude Opus 4.6 | 1M tokens | 32K tokens (300K via beta) | Complex multi-step tasks |
| **Claude Sonnet 4.6** | 1M tokens | 64K tokens | Balanced — everyday coding, RAG, high-throughput workflows |
| Claude Sonnet 4.5 | 200K tokens | 8K tokens | Mid-tier, fast inference |
| **Claude Haiku 4.5** | 200K tokens | 8K tokens | Fastest, cheapest — high-volume simple tasks, classification |

**Key Notes:**
- Opus 4.6/4.7/4.8 and Sonnet 4.6 support **1M token context** — can handle entire codebases or books
- **300K output** available on Opus and Sonnet 4.6 via the `output-300k-2026-03-24` beta header (Message Batches API)
- Server-side compaction (beta) available on Opus 4.6/4.7/4.8 and Sonnet 4.6 for very long conversations
- Extended thinking consumes internal tokens that count toward the output limit
- Streaming supported on all models

---

## 2. OpenAI / Azure OpenAI Models

### GPT-5.x Frontier Series (2026)

| Model | Context Window | Max Output | Pricing (Input / Output) | Best Use Case |
|---|---|---|---|---|
| **GPT-5.5** | 1,050,000 tokens | 128K tokens | Premium | Coding, professional work — new class of intelligence |
| **GPT-5.5 Pro** | 1,050,000 tokens | 128K tokens | Highest | Smarter and more precise than GPT-5.5 |
| **GPT-5.4** | 1,000,000 tokens | 128K tokens | $2.50 / $15.00 per 1M | Capable frontier model, professional work |
| **GPT-5.4 Pro** | 1,000,000 tokens | 128K tokens | $30.00 / $180.00 per 1M | Smarter and more precise than GPT-5.4 |
| **GPT-5.4 Mini** | 400,000 tokens | 128K tokens | $0.75 / $4.50 per 1M | Strongest mini — coding, computer use, subagents |
| **GPT-5.4 Nano** | 400,000 tokens | 128K tokens | $0.20 / $1.25 per 1M | Cheapest GPT-5.4-class model, simple high-volume tasks |
| GPT-5.1 | 200K tokens | 100K tokens | — | Reasoning, math, code |
| GPT-5.1 Mini | 128K tokens | 65K tokens | — | Lightweight reasoning tasks |

> **Pricing note:** For GPT-5.4 and GPT-5.5, prompts exceeding **272K tokens** are billed at **2× input and 1.5× output** for the full session.

### GPT-4.x Legacy Series

| Model | Context Window | Max Output | Best Use Case |
|---|---|---|---|
| GPT-4o | 128K tokens | 16K tokens | Multimodal (text + image), RAG, agents |
| GPT-4o mini | 128K tokens | 16K tokens | Cheap, fast alternative to GPT-4o |
| GPT-4 Turbo | 128K tokens | 4K tokens | Long document analysis |
| GPT-3.5 Turbo | 16K tokens | 4K tokens | Simple tasks, fast prototyping |
| o1 | 200K tokens | 100K tokens | Deep reasoning, math, code |
| o3 | 200K tokens | 100K tokens | Advanced reasoning, research |
| o3-mini | 200K tokens | 65K tokens | Fast reasoning at lower cost |

**Azure OpenAI specific notes:**
- Models deployed per region — not all GPT-5.x models available in all Azure regions yet
- TPM quota set at deployment level in Azure portal — default is often 10K–30K TPM
- Request quota increases: Azure Portal → Your Resource → Quotas → Request increase
- Azure adds a small network latency overhead vs. OpenAI direct API

---

## 3. Google Gemini Models (Latest 2026)

### Flagship / Frontier Models

| Model | Context Window | Max Output | Price (Input / Output) | Best Use Case |
|---|---|---|---|---|
| **Gemini 3.5 Flash** | 1M tokens | 66K tokens | $1.50 / $9.00 | Latest agentic model — frontier-level multi-step tasks, coding, 4× speed |
| **Gemini 3.1 Pro** | 2M tokens | 66K tokens | $2 / $12 (<200K ctx) · $4 / $18 (>200K) | Most capable — complex reasoning, broad world knowledge |
| **Gemini 3.1 Flash** | 1M tokens | 66K tokens | $0.75 / $4.50 | Balanced speed + quality — everyday tasks, agents |
| **Gemini 3.1 Flash-Lite** | 1M tokens | 66K tokens | $0.25 / $1.50 | Cheapest Gemini — high-volume, cost-effective tasks (2.5× faster than 2.5 Flash) |
| Gemini 2.0 Flash | 1M tokens | 8K tokens | $0.10 / $0.40 | Previous gen fast model (still in wide use) |
| Gemini 1.5 Pro | 2M tokens | 8K tokens | $1.25 / $5 | Previous gen 2M-context model |

### Specialized / Media Models

| Model | Type | Best Use Case |
|---|---|---|
| **Gemini 3.1 Flash Live** | Real-time audio + video streaming | Ultra-low latency live conversations, bidirectional video agents |
| **Imagen 4** | Text-to-image (4K) | Ultra-fast high-res image generation, best text rendering |
| **Veo 3.1** | Text-to-video | State-of-the-art cinematic video generation |
| **Nano Banana 2** | On-device vision | High-efficiency visual creation on-device (edge / mobile) |

**Notes:**
- Gemini 3.1 Pro's **2M context** is the largest of any production frontier model (as of mid-2026)
- Batch inference on all Gemini models: **50% off**
- Context caching: **up to 90% off** repeated input tokens
- Native multimodal: text, image, video, audio across the entire Gemini 3.x family
- Gemini 3.5 Flash is the recommended default for most new GCP workloads in 2026

---

## 4. Frontier Open-Source & Third-Party Models (2026)

### MiniMax M3
| Spec | Value |
|---|---|
| Context Window | 1,000,000 tokens |
| Capabilities | Vision, Tools, Thinking, Cloud |
| Best For | Coding & agentic frontier tasks, multimodal workflows |
| Access | Cloud API |

- Native multimodality (text + image + tool calls)
- Designed for long-context agentic tasks

---

### Gemma 4 (Google DeepMind — Open Source)
| Variant | Context Window | Capabilities |
|---|---|---|
| E2B / E4B (edge) | 128K tokens | Vision, Tools, Thinking, Audio |
| 12B / 26B / 31B | 256K tokens | Vision, Tools, Thinking, Audio, Cloud |

- Delivers frontier-level performance at each size
- Well-suited for reasoning, agentic workflows, coding, and multimodal understanding
- Free to download and self-host via Hugging Face / Ollama

---

### Qwen 3.5 (Alibaba — Open Source)
| Variant | Context Window | Capabilities |
|---|---|---|
| 0.8B / 2B / 4B | 262K tokens | Tools, Thinking |
| 9B / 27B / 35B / 122B | 262K tokens | Vision, Tools, Thinking, Cloud |

- Exceptional utility across text, code, and multimodal tasks
- Sizes from 0.8B (edge/mobile) to 122B (frontier quality)
- Supports tool calling and extended thinking natively

---

### Qwen 3.6 (Alibaba — Open Source)
| Variant | Context Window | Max Output | Capabilities |
|---|---|---|---|
| Qwen 3.6 27B / 35B | 262K tokens native | 32K tokens | Vision, Tools, Thinking |
| **Qwen 3.6 Plus** | 1,000,000 tokens | 65,536 tokens | Vision, Tools, Thinking, Cloud |

- Substantial upgrades in agentic coding and thinking preservation over Qwen 3.5
- Qwen 3.6 Plus extends to 1M context with 65K output — matches frontier closed models

---

### NVIDIA Nemotron 3 Ultra
| Spec | Value |
|---|---|
| Context Window | 1,000,000 tokens |
| Capabilities | Tools, Thinking, Cloud |
| Best For | High-throughput reasoning, long-running agent workflows |
| Access | NVIDIA Cloud / NIM API |

- Built for enterprise agentic pipelines
- Optimized for structured tool calling and multi-step reasoning

---

### Liquid AI LFM2.5-8B-A1B
| Spec | Value |
|---|---|
| Parameters | 8.3B total / 1.5B active (MoE) |
| Context Window | 128K tokens |
| Capabilities | Tools, Thinking |
| Best For | Edge deployment, fast reliable tool calling on consumer hardware |
| Access | Self-hosted / Hugging Face |

- On-device Mixture of Experts — runs efficiently on consumer GPUs
- Trained on 28T tokens with scaled reinforcement learning
- 128K context is unusually large for an on-device model of this class

---

## 5. Meta Llama (Open Source / Self-hosted)

| Model | Context Window | Best Use Case |
|---|---|---|
| Llama 3.1 8B | 128K tokens | Lightweight local deployment |
| Llama 3.1 70B | 128K tokens | Mid-tier local or cloud |
| Llama 3.1 405B | 128K tokens | Best open-source quality |
| Llama 3.2 3B / 11B | 128K tokens | Edge / mobile devices |
| Llama 3.3 70B | 128K tokens | Near-GPT-4 quality at lower cost |

- Free to run locally using Ollama, vLLM, or Hugging Face
- No API rate limits when self-hosted

---

## 6. Mistral Models

| Model | Context Window | Best Use Case |
|---|---|---|
| Mistral 7B | 32K tokens | Lightweight, fast inference |
| Mistral Large | 128K tokens | Complex reasoning, coding |
| Mixtral 8x7B | 32K tokens | Open-source MoE, efficient |
| Codestral | 32K tokens | Code generation |

---

## 7. API Rate Limits

### Key Terms

| Term | Full Form | Meaning |
|---|---|---|
| **TPM** | Tokens Per Minute | Total number of tokens (input + output combined) you can send/receive across all requests in a 60-second rolling window. Hitting this limit returns a **429 error** even if your RPM is fine. |
| **RPM** | Requests Per Minute | Total number of individual API calls you can make in a 60-second rolling window. One call = one request, regardless of how many tokens it contains. |
| **TPD** | Tokens Per Day | Total tokens allowed across all requests in a 24-hour period. A daily hard cap — once hit, all requests are blocked until the next day resets. Common on free tiers. |

**How they interact:**
```
You have: TPM = 40,000 · RPM = 500 · TPD = 300,000

Send 10 requests × 4,000 tokens each in one minute
→ Uses 40,000 TPM  ✅ (at limit)
→ Uses 10 RPM      ✅ (fine)
→ Uses 40,000 TPD  ✅ (fine for now, 260,000 remaining today)

Send 1 request × 50,000 tokens
→ 429 error — exceeds TPM limit even though RPM is fine
```

**Practical tips:**
- **429 on TPM** → your prompts are too large or too frequent — reduce chunk size or add delays
- **429 on RPM** → you're making too many calls — batch requests or add rate limiting in code
- **429 on TPD** → you've exhausted the daily budget — upgrade tier or wait for reset

---

### Anthropic (Claude API)

| Tier | Model | RPM | TPM | TPD |
|---|---|---|---|---|
| Free | Haiku 4.5 | 5 | 25,000 | 300,000 |
| Free | Sonnet 4.6 | 5 | 40,000 | 300,000 |
| Free | Opus 4.x | 5 | 10,000 | 300,000 |
| Build (Paid) | Haiku 4.5 | 1,000 | 100,000 | Unlimited |
| Build (Paid) | Sonnet 4.6 | 1,000 | 80,000 | Unlimited |
| Build (Paid) | Opus 4.x | 500 | 40,000 | Unlimited |

### OpenAI API

| Tier | RPM | TPM | Unlock Condition |
|---|---|---|---|
| Free | 3 | 40,000 | Default |
| Tier 1 | 500 | 200,000 | $5 spent |
| Tier 2 | 5,000 | 2,000,000 | $50 spent |
| Tier 3 | 5,000 | 4,000,000 | $100 spent |
| Tier 4 | 10,000 | 10,000,000 | $250 spent |
| Tier 5 | 10,000 | 30,000,000 | $1,000 spent |

### Azure OpenAI (Default Quotas — per deployment)

| Model | TPM (default) | RPM (default) |
|---|---|---|
| GPT-4o | 30,000 | 180 |
| GPT-4 Turbo | 10,000 | 60 |
| GPT-3.5 Turbo | 120,000 | 720 |

- Increase via: Azure Portal → Your Resource → Quotas → Request increase
- For very high load, deploy to multiple regions

---

## 8. What Happens When You Hit a Limit

| Error | Meaning | Fix |
|---|---|---|
| 429 | Rate limit exceeded | Retry with exponential backoff |
| 400 | Prompt too long (context exceeded) | Reduce input, chunk documents |
| 500 | Server error | Retry after short delay |
| 503 | Service unavailable | Retry, or switch to fallback model |

**Exponential backoff example:**
```python
import time
import random

def call_with_retry(func, max_retries=5):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e):
                wait = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")
```

---

## 9. When to Use Input vs Output Tokens

### Input Tokens (what you send)
- System prompt
- Conversation history (chat memory)
- Retrieved RAG documents
- User's question
- Tool / function definitions

**Tips:**
- Trim chat history to last N messages to stay within context limits
- Send only top-K most relevant RAG chunks
- Use prompt caching (Anthropic / Azure Semantic Cache) to cut repeated input costs

### Output Tokens (what the model generates)
- The model's response text
- Tool call arguments generated by the model
- Chain-of-thought / reasoning tokens (extended thinking models)

**Tips:**
- Set `max_tokens` to cap output and prevent runaway costs
- Structured output (JSON mode) uses fewer tokens than free-form prose
- Streaming reduces perceived latency for long outputs

---

## 10. Context Window Strategy for RAG Chatbots

```
Total context = system_prompt + chat_history + rag_chunks + user_query + buffer
```

| Component | Recommended Token Budget |
|---|---|
| System prompt | 500 – 1,000 tokens |
| Chat history | Last 5–10 turns (~2,000–4,000 tokens) |
| RAG retrieved chunks | 2,000 – 6,000 tokens |
| User query | 50 – 500 tokens |
| Safety buffer | ~500 tokens |
| **Total target** | **< 80% of model's context limit** |

**Why 80% and not 100%?**
- Leaves room for model output
- Models degrade in quality near the end of their context window
- Prevents unexpected 400 errors from slight overflows

---

## 11. Cost-Aware Model Selection

| Task | Recommended Model | Why |
|---|---|---|
| Simple Q&A, classification | GPT-5.4 Nano / Claude Haiku 4.5 | Cheapest, fast |
| RAG with moderate docs | GPT-5.4 Mini / Claude Sonnet 4.6 | Balanced quality/cost |
| Complex reasoning, coding | Claude Opus 4.8 / GPT-5.5 Pro | Best accuracy |
| Very long documents (>200K tokens) | Claude Opus 4.8 / Qwen 3.6 Plus / GPT-5.4 | 1M context support |
| Real-time chat | GPT-5.4 Nano / Claude Haiku 4.5 | Lowest latency, lowest cost |
| Edge / on-device | LFM2.5-8B-A1B / Gemma 4 E4B / Qwen 3.5 0.8B | Runs on consumer hardware |
| Local / private data | Llama 3.3 70B / Qwen 3.6 / Gemma 4 (self-hosted) | No data leaves your infra |
| Multimodal (image + text) | GPT-5.5 / Claude Opus 4.8 / MiniMax M3 / Gemma 4 | Native vision support |
| Agentic long-running workflows | Claude Opus 4.8 / Nemotron 3 Ultra / GPT-5.4 | Best tool use + long context |

---

## 12. Quick Reference — Context Limits at a Glance

```
2,000,000  tokens  →  Gemini 3.1 Pro                     (~1,500,000 words)
2,000,000  tokens  →  Gemini 1.5 Pro (prev gen)          (~1,500,000 words)
1,050,000  tokens  →  GPT-5.5, GPT-5.5 Pro               (~787,500 words)
1,000,000  tokens  →  Gemini 3.5 Flash, 3.1 Flash        (~750,000 words)
1,000,000  tokens  →  Claude Opus 4.6/4.7/4.8            (~750,000 words)
1,000,000  tokens  →  Claude Sonnet 4.6                   (~750,000 words)
1,000,000  tokens  →  GPT-5.4, GPT-5.4 Pro               (~750,000 words)
1,000,000  tokens  →  MiniMax M3, Nemotron 3 Ultra        (~750,000 words)
1,000,000  tokens  →  Qwen 3.6 Plus                       (~750,000 words)
  400,000  tokens  →  GPT-5.4 Mini, GPT-5.4 Nano         (~300,000 words)
  262,000  tokens  →  Qwen 3.5, Qwen 3.6 (native)        (~196,500 words)
  256,000  tokens  →  Gemma 4 (12B/26B/31B)              (~192,000 words)
  200,000  tokens  →  Claude Haiku 4.5 / Sonnet 4.5       (~150,000 words)
  128,000  tokens  →  GPT-4o, Llama 3.1, Gemma 4 edge    (~96,000 words)
  128,000  tokens  →  LFM2.5-8B-A1B                       (~96,000 words)
   32,000  tokens  →  Mistral 7B                           (~24,000 words)
   16,000  tokens  →  GPT-3.5 Turbo                        (~12,000 words)
```

---

## 13. AWS Bedrock

AWS Bedrock is a **fully managed service** that gives access to foundation models from multiple providers via a single AWS API — no infrastructure to manage.

### Model Families Available on Bedrock

| Provider | Models | Strengths |
|---|---|---|
| **Anthropic** | Claude Opus 4.7/4.8, Sonnet 4.6, Haiku 4.5 | Best reasoning, long-context, agentic coding |
| **Amazon Nova** | Nova Micro, Lite, Pro, Premier | Cost-optimized, tight AWS integration |
| **Meta Llama** | Llama 4 Maverick, Llama 4 Scout, Llama 3.3 70B | Open weights, general purpose |
| **Mistral** | Mistral Large, Mistral Small | Multilingual, coding |
| **Cohere** | Command R, Command R+ | Enterprise RAG, retrieval-focused |
| **Amazon Titan** | Titan Text, Titan Embeddings V2 | Cheap, native AWS, embedding anchor |
| **Stability AI** | Stable Diffusion | Image generation |

### Amazon Nova Models (Amazon's Own)
| Model | Best Use Case |
|---|---|
| Nova Micro | Fastest, text-only, lowest cost |
| Nova Lite | Multimodal, fast, affordable |
| Nova Pro | High accuracy, complex multimodal tasks |
| Nova Premier | Most capable Amazon model, long-context agents |

### AWS Bedrock Key Services
| Service | What It Does |
|---|---|
| **Bedrock Knowledge Bases** | Managed RAG — connect S3 docs, auto-chunks, embeds, stores in vector DB |
| **Bedrock Agents** | Build multi-step AI agents with tool use and memory |
| **Bedrock Guardrails** | Content filtering, PII detection, hallucination detection |
| **Bedrock Model Evaluation** | Run automated evals on your models |
| **Bedrock Flows** | Visual workflow builder for LLM pipelines |

### When to Choose Bedrock
- Already on AWS infrastructure (IAM, S3, Lambda)
- Need compliance (SOC2, HIPAA, GDPR) with familiar AWS controls
- Want managed RAG without building your own vector pipeline
- Multi-model flexibility from a single API

---

## 14. Azure AI Foundry

Azure AI Foundry is Microsoft's **unified platform** for building, deploying, and managing AI applications. It supersedes and consolidates Azure OpenAI Service and Azure Machine Learning Studio into one surface.

### Azure AI Foundry vs Azure OpenAI Service

| | Azure OpenAI Service | Azure AI Foundry |
|---|---|---|
| **Scope** | OpenAI models only | OpenAI + Microsoft + 3rd-party models |
| **Model Catalog** | GPT-4o, GPT-5.x, Whisper, DALL-E | All OpenAI + Phi-4, Llama, Mistral, Cohere, etc. |
| **Agent Support** | Limited | Full agent workflows, multi-agent orchestration |
| **Evaluation** | No built-in | Built-in model evaluation and monitoring |
| **Fine-tuning** | Basic | Advanced fine-tuning and RLHF |
| **Best For** | Simple GPT API calls | Full AI application lifecycle management |

### Models in Azure AI Foundry Model Catalog

| Provider | Models |
|---|---|
| OpenAI | GPT-5.5, GPT-5.4, GPT-4o, o3, DALL-E, Whisper |
| Microsoft | Phi-4, Phi-3.5, Phi-3 Mini (SLMs) |
| Meta | Llama 4, Llama 3.3 |
| Mistral AI | Mistral Large, Mistral Small |
| Cohere | Command R, Command R+ |
| NVIDIA | Nemotron models |

### Microsoft Phi Models (Small Language Models)
| Model | Params | Best Use Case |
|---|---|---|
| Phi-4 | 14B | Low-latency, reasoning, coding — efficient alternative to GPT-4o |
| Phi-3.5 Mini | 3.8B | Edge / mobile deployment |
| Phi-3 Mini | 3.8B | On-device, fast inference, Windows Copilot+ |

### Azure AI Foundry Key Services
| Service | What It Does |
|---|---|
| **Azure AI Search** | Vector + keyword hybrid search, RAG backbone |
| **Azure Content Safety** | Detects harmful content, PII, prompt injections |
| **Prompt Flow** | Visual LLM pipeline builder with evaluation |
| **Azure AI Document Intelligence** | Extract tables, forms, diagrams from PDFs |
| **Azure AI Speech** | STT / TTS, real-time transcription |
| **Azure ML** | Model training, fine-tuning, MLOps |

---

## 15. Embedding Models

Embedding models convert text (or images) into **dense numerical vectors**. These vectors capture semantic meaning — similar texts produce vectors that are close together in vector space. Embeddings power semantic search, RAG retrieval, clustering, and classification.

```
"The cat sat on the mat"  →  [0.21, -0.43, 0.87, ...]  (384 or 1536 numbers)
"A feline rested on a rug" →  [0.19, -0.41, 0.85, ...]  (very close → similar meaning)
```

### Paid / Cloud Embedding Models

| Provider | Model | Dimensions | Context | Notes |
|---|---|---|---|---|
| **OpenAI / Azure** | text-embedding-3-small | 1,536 | 8K tokens | Best cost/quality balance, most widely used |
| **OpenAI / Azure** | text-embedding-3-large | 3,072 | 8K tokens | Highest quality OpenAI embedding |
| **OpenAI / Azure** | text-embedding-ada-002 | 1,536 | 8K tokens | Legacy, replaced by v3 models |
| **AWS Bedrock** | Amazon Titan Embeddings V2 | 1,024 | 8K tokens | Native AWS, cost-effective, multilingual |
| **AWS Bedrock** | Cohere Embed v3 | 1,024 | 512 tokens | Best for retrieval tasks, multilingual |
| **Google Vertex AI** | text-embedding-004 | 768 | 2K tokens | Google's current recommended embedding |
| **Google Vertex AI** | textembedding-gecko@003 | 768 | 3K tokens | Older but widely used |
| **Voyage AI** | voyage-3 | 1,024 | 32K tokens | Top MTEB scores, great for RAG |
| **Cohere** | embed-english-v3.0 | 1,024 | 512 tokens | Strong for English retrieval |

### Open-Source / HuggingFace Embedding Models

| Model | Dimensions | Context | Size | Best For |
|---|---|---|---|---|
| **all-MiniLM-L6-v2** | 384 | 512 tokens | 22M params | Fast, lightweight — best for prototyping / edge |
| **all-MiniLM-L12-v2** | 384 | 512 tokens | 33M params | Slightly better quality than L6, still fast |
| **all-mpnet-base-v2** | 768 | 512 tokens | 109M params | Better quality, semantic search |
| **bge-small-en-v1.5** | 384 | 512 tokens | 33M params | Fast, good quality for English |
| **bge-base-en-v1.5** | 768 | 512 tokens | 109M params | Mid-tier, strong retrieval |
| **bge-large-en-v1.5** | 1,024 | 512 tokens | 335M params | High quality English retrieval |
| **BAAI/bge-m3** | 1,024 | 8K tokens | 570M params | Multilingual, long-context, #1 most downloaded |
| **nomic-embed-text-v1.5** | 768 | 8K tokens | 137M params | Open-source, long context, MoE architecture |
| **e5-large-v2** | 1,024 | 512 tokens | 335M params | Strong on MTEB benchmark |
| **Qwen3-Embedding** | 1,024–7K | 32K tokens | Multiple sizes | Best open-weight MTEB scores as of 2026 |
| **gte-large** | 1,024 | 512 tokens | 335M params | Strong general embedding |

### Quick Comparison: allMiniLM vs BGE vs Nomic

| | all-MiniLM-L6-v2 | bge-m3 | nomic-embed-text |
|---|---|---|---|
| Dimensions | 384 | 1,024 | 768 |
| Context | 512 tokens | 8,192 tokens | 8,192 tokens |
| Language | English | Multilingual | Multilingual |
| Speed | Very fast | Moderate | Fast |
| Quality | Good (prototype) | Excellent (production) | Very good |
| License | Apache 2.0 | MIT | Apache 2.0 |
| Use case | Local dev, edge | Production RAG | Long-doc RAG |

### How to Use (LangChain)
```python
# OpenAI (paid)
from langchain_openai import AzureOpenAIEmbeddings
embeddings = AzureOpenAIEmbeddings(model="text-embedding-3-small")

# HuggingFace (free, local)
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# AWS Bedrock (paid)
from langchain_aws import BedrockEmbeddings
embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
```

---

## 16. Databases — SQL, NoSQL, and Vector

---

### SQL (Relational Databases)

**What it is:** Data stored in structured tables with rows and columns. Relationships between tables are enforced via foreign keys. Uses **SQL** (Structured Query Language) to query data.

**Key properties (ACID):**
- **A**tomicity — transaction fully completes or fully rolls back
- **C**onsistency — data always valid per defined rules
- **I**solation — concurrent transactions don't interfere
- **D**urability — committed data survives crashes

**When to use:**
- Structured, predictable data (users, orders, invoices)
- Complex joins across multiple tables
- Strong consistency required (banking, healthcare)

| Database | Notes |
|---|---|
| **PostgreSQL** | Most feature-rich open-source SQL DB; supports JSON, vectors via pgvector |
| **MySQL / MariaDB** | Fast reads, widely used in web apps |
| **SQLite** | Serverless, file-based — perfect for local dev and edge apps |
| **Microsoft SQL Server** | Enterprise-grade, native Azure integration |
| **Amazon RDS / Aurora** | Managed SQL on AWS (PostgreSQL or MySQL engine) |

---

### NoSQL (Non-Relational Databases)

**What it is:** Flexible schema databases designed for scale, speed, and unstructured or semi-structured data. "NoSQL" does NOT mean "no SQL ever" — it means "not only SQL."

**When to use:**
- Variable or evolving schema (user profiles with different fields)
- High-volume reads/writes at scale
- Distributed, globally replicated data
- Hierarchical or nested data structures

#### NoSQL Types and Examples

| Type | How Data is Stored | Examples | Best For |
|---|---|---|---|
| **Document** | JSON-like documents in collections | MongoDB, Firestore, CouchDB | User profiles, product catalogs, CMS |
| **Key-Value** | Simple key → value pairs | Redis, DynamoDB, Memcached | Caching, sessions, leaderboards |
| **Column-Family** | Rows with dynamic column sets | Cassandra, HBase, ScyllaDB | Time-series, IoT, write-heavy workloads |
| **Graph** | Nodes and edges (relationships) | Neo4j, Amazon Neptune, ArangoDB | Social networks, fraud detection, knowledge graphs |
| **Time-Series** | Timestamped data optimized for range queries | InfluxDB, TimescaleDB, QuestDB | Metrics, logs, sensor data |

#### SQL vs NoSQL — Key Differences

| | SQL | NoSQL |
|---|---|---|
| Schema | Fixed, predefined | Flexible, dynamic |
| Scaling | Vertical (bigger machine) | Horizontal (more machines) |
| Consistency | Strong (ACID) | Eventual (CAP theorem trade-off) |
| Joins | Easy, built-in | Manual / application-level |
| Query language | SQL (standardized) | Varies per DB |
| Best for | Structured, relational data | Scale, flexibility, unstructured data |

---

### Vector Databases

**What it is:** A database optimized for storing and searching **high-dimensional vectors** (embeddings). Instead of exact matches like SQL, it finds the **nearest neighbors** — vectors that are semantically closest to a query vector.

**Why it exists:** Traditional databases can't efficiently search across millions of 1024-dimensional float arrays. Vector DBs use specialized indexing algorithms (HNSW, IVF) to do this in milliseconds.

#### How Vector Search Works Internally

```
1. EMBED   — Convert your text/image to a vector using an embedding model
             "What is RAG?" → [0.21, -0.43, 0.87, ..., 0.12]  (1024 numbers)

2. STORE   — Save vectors + metadata in the vector DB with an index

3. QUERY   — Convert user's question to a vector the same way

4. SEARCH  — Find top-K vectors closest to the query vector
             using similarity: cosine similarity, dot product, or L2 distance

5. RETURN  — Return the original text chunks associated with those vectors
```

#### Similarity Metrics

| Metric | Formula | When to Use |
|---|---|---|
| **Cosine Similarity** | angle between vectors | Most common — normalized text embeddings |
| **Dot Product** | magnitude × direction | When vectors aren't normalized |
| **Euclidean (L2)** | straight-line distance | Image embeddings, spatial data |

#### HNSW Index — How It Works Internally

HNSW (Hierarchical Navigable Small World) is the dominant indexing algorithm in all major vector DBs.

```
Layer 2 (sparse):   A ————————————— E
                         \
Layer 1 (medium):   A — B — C — D — E
                               |
Layer 0 (all nodes): A-B-C-D-[E]-F-G-H  ← final precision search here
```

- Vectors are organized into **multiple graph layers**
- **Upper layers** = sparse — big jumps across the space (rough navigation)
- **Bottom layer** = all nodes — fine-grained neighbor search
- Search starts at the top, greedily moves toward the query, drops down a layer, repeats
- Insertion assigns each new vector a random max-layer and connects it to its neighbors
- Search complexity: **O(log N)** — fast even at billions of vectors

#### IVF (Inverted File Index) — Alternative to HNSW

- Divides vector space into clusters (Voronoi cells) using k-means
- At query time, only searches the closest clusters, not all vectors
- Faster for very large datasets; less accurate than HNSW at the same recall level
- Used by FAISS

---

### Vector Database Comparison

| Database | Type | Language | Best For | Hosting |
|---|---|---|---|---|
| **Pinecone** | Managed only | — | Production, enterprise, auto-scaling | Cloud only |
| **Qdrant** | Open source + cloud | Rust | Fastest latency (~4ms p50), filtering, production | Self-host or cloud |
| **Weaviate** | Open source + cloud | Go | Hybrid search (vector + keyword), built-in vectorizers | Self-host or cloud |
| **Milvus / Zilliz** | Open source + cloud | C++/Go | Billion-scale, GPU search, enterprise | Self-host or cloud |
| **Chroma** | Open source | Python | Local dev, prototyping, simplest API | Local or self-host |
| **FAISS** | Library (not a DB) | C++/Python | In-memory search, research, no persistence | Embedded/local |
| **pgvector** | PostgreSQL extension | SQL | Adding vector search to existing Postgres DB | Self-host or managed |
| **Redis VSS** | Extension of Redis | C | Caching + vector search in one, low latency | Self-host or cloud |
| **LanceDB** | Open source | Rust | Serverless, embedded, great for notebooks/local RAG | Local or cloud |

#### Detailed Differences

| | Pinecone | Qdrant | Chroma | pgvector |
|---|---|---|---|---|
| Setup | SaaS, instant | Docker / pip | pip install | Postgres extension |
| Latency | ~8ms p50 | ~4ms p50 | Variable | Depends on Postgres |
| Filtering | Yes | Best-in-class | Basic | Full SQL |
| Persistence | Yes | Yes | Optional | Yes (Postgres) |
| Cost | Paid | Free self-host | Free | Free |
| Production ready | Yes | Yes | Dev only | Yes (with tuning) |
| Transactions | No | No | No | Yes (ACID) |

#### When to Use Which

| Scenario | Best Choice |
|---|---|
| Prototyping / learning RAG | **Chroma** (simplest) |
| Production RAG, fast setup | **Pinecone** (managed) or **Qdrant** (self-hosted) |
| Already using PostgreSQL | **pgvector** (no extra service) |
| Billion+ vectors, GPU search | **Milvus / Zilliz** |
| Hybrid search (vector + keyword) | **Weaviate** or **Azure AI Search** |
| Caching + vector in one layer | **Redis VSS** |
| Local notebooks, no server | **FAISS** or **LanceDB** |

#### Code Example — Chroma (Simplest)
```python
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings

client = chromadb.Client()
collection = client.create_collection("my_docs")

# Add documents
collection.add(
    documents=["RAG stands for Retrieval Augmented Generation", "LangGraph is a library for agents"],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(query_texts=["What is RAG?"], n_results=2)
```

#### Code Example — Qdrant (Production)
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(url="http://localhost:6333")
client.create_collection(
    collection_name="my_docs",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
)
```

---

## 17. Full Stack Reference — RAG Pipeline Components

```
User Query
    ↓
[Embedding Model]  →  Query Vector
    ↓
[Vector Database]  →  Top-K Similar Chunks  (Qdrant / Pinecone / pgvector)
    ↓
[LLM]              →  Final Answer          (Claude / GPT-5.4 / Llama)
    ↓
[SQL / NoSQL DB]   →  User history, metadata, sessions  (PostgreSQL / MongoDB)
```

| Layer | Open Source Option | Paid/Managed Option |
|---|---|---|
| Embedding | bge-m3, all-MiniLM | text-embedding-3-small (OpenAI/Azure) |
| Vector DB | Qdrant, Chroma, pgvector | Pinecone, Weaviate Cloud, Azure AI Search |
| LLM | Llama 3.3 70B, Qwen 3.6 | Claude Sonnet 4.6, GPT-5.4 |
| Document store | MongoDB, SQLite | DynamoDB, Cosmos DB, Firestore |
| Orchestration | LangChain, LlamaIndex | Azure AI Foundry, AWS Bedrock Agents |

---

## 18. Platform Mega-Comparison — Azure vs AWS vs GCP vs Open Source

> Quick-read interview reference. One table per topic, then use-case guide at the end.

---

### 18A. LLM Models by Platform

| Model | Azure AI Foundry | AWS Bedrock | GCP Vertex AI | Open Source (Ollama / HF) |
|---|---|---|---|---|
| **GPT-5.5 / 5.5 Pro** | ✅ | ❌ | ❌ | ❌ |
| **GPT-5.4 / Mini / Nano** | ✅ | ❌ | ❌ | ❌ |
| **GPT-4o** | ✅ | ❌ | ❌ | ❌ |
| **Claude Opus 4.7 / 4.8** | ❌ | ✅ | ✅ (via Model Garden) | ❌ |
| **Claude Sonnet 4.6** | ❌ | ✅ | ✅ (via Model Garden) | ❌ |
| **Claude Haiku 4.5** | ❌ | ✅ | ✅ (via Model Garden) | ❌ |
| **Gemini 3.5 Flash** ⭐ | ❌ | ❌ | ✅ | ❌ |
| **Gemini 3.1 Pro (2M ctx)** | ❌ | ❌ | ✅ | ❌ |
| **Gemini 3.1 Flash** | ❌ | ❌ | ✅ | ❌ |
| **Gemini 3.1 Flash-Lite** | ❌ | ❌ | ✅ | ❌ |
| **Gemini 3.1 Flash Live** | ❌ | ❌ | ✅ | ❌ |
| **Imagen 4** (image gen) | ❌ | ❌ | ✅ | ❌ |
| **Veo 3.1** (video gen) | ❌ | ❌ | ✅ | ❌ |
| Gemini 2.0 Flash (prev gen) | ❌ | ❌ | ✅ | ❌ |
| **Amazon Nova Pro / Lite / Micro** | ❌ | ✅ | ❌ | ❌ |
| **Phi-4 (Microsoft SLM)** | ✅ | ❌ | ❌ | ✅ (HuggingFace) |
| **Llama 4 Maverick / Scout** | ✅ | ✅ | ✅ (Model Garden) | ✅ (Ollama) |
| **Llama 3.3 70B** | ✅ | ✅ | ✅ | ✅ (Ollama) |
| **Mistral Large** | ✅ | ✅ | ✅ | ✅ (Ollama) |
| **Qwen 3.5 / 3.6** | ❌ | ❌ | ❌ | ✅ (Ollama / HF) |
| **Gemma 4** | ❌ | ❌ | ✅ (native) | ✅ (Ollama / HF) |
| **Command R / R+** | ❌ | ✅ | ❌ | ✅ (HF) |

---

### 18B. Embedding Models by Platform

| Model | Provider | Dimensions | Context | Price / 1M tokens | Platform |
|---|---|---|---|---|---|
| **text-embedding-3-small** | OpenAI | 1,536 | 8K | $0.02 | Azure / OpenAI API |
| **text-embedding-3-large** | OpenAI | 3,072 | 8K | $0.13 | Azure / OpenAI API |
| **text-embedding-ada-002** | OpenAI | 1,536 | 8K | $0.10 | Azure (legacy) |
| **Amazon Titan Embeddings V2** | AWS | 1,024 | 8K | $0.10 | AWS Bedrock |
| **Cohere Embed v3** | Cohere | 1,024 | 512 | $0.10 | AWS Bedrock / API |
| **text-embedding-004** | Google | 768 | 2K | $0.10 | GCP Vertex AI |
| **Gemini Embedding** | Google | 3,072 | 8K | $0.15 | GCP Vertex AI |
| **all-MiniLM-L6-v2** | HuggingFace | 384 | 512 | **FREE** | Ollama / HF / local |
| **all-MiniLM-L12-v2** | HuggingFace | 384 | 512 | **FREE** | Ollama / HF / local |
| **all-mpnet-base-v2** | HuggingFace | 768 | 512 | **FREE** | Ollama / HF / local |
| **bge-m3** | BAAI / HF | 1,024 | 8K | **FREE** | Ollama / HF / local |
| **bge-large-en-v1.5** | BAAI / HF | 1,024 | 512 | **FREE** | HF / local |
| **nomic-embed-text-v1.5** | Nomic / HF | 768 | 8K | **FREE** | Ollama / HF / local |
| **Qwen3-Embedding** | Alibaba / HF | 1,024–7K | 32K | **FREE** | HF / local |
| **e5-large-v2** | Microsoft / HF | 1,024 | 512 | **FREE** | HF / local |

---

### 18C. Services — LLM, Vector Store, Storage, Orchestration

| Category | Azure | AWS | GCP | Open Source |
|---|---|---|---|---|
| **LLM API** | Azure AI Foundry / Azure OpenAI | AWS Bedrock | Vertex AI (Gemini API) | Ollama, vLLM, HuggingFace Inference |
| **SLM / Edge LLM** | Phi-4 on Azure | Nova Micro | Gemma 4 | Ollama (Phi, Gemma, Qwen) |
| **Vector Store** | Azure AI Search | Amazon OpenSearch / Aurora pgvector | Vertex AI Vector Search / AlloyDB pgvector | Qdrant, Chroma, FAISS, pgvector |
| **Managed RAG** | Azure AI Search + Prompt Flow | Bedrock Knowledge Bases | Vertex AI RAG Engine | LangChain + Chroma / Qdrant |
| **Agent Framework** | Azure AI Foundry Agents | Bedrock Agents | Vertex AI Agents / Agentspace | LangGraph, AutoGen, CrewAI |
| **Embedding Service** | Azure OpenAI (text-embedding-3) | Bedrock (Titan / Cohere Embed) | Vertex AI (text-embedding-004) | HuggingFace local models |
| **Document Extraction** | Azure AI Document Intelligence | Textract | Document AI | Docling, Unstructured |
| **Object / File Storage** | Azure Blob Storage | Amazon S3 | Google Cloud Storage (GCS) | MinIO (S3-compatible, self-hosted) |
| **SQL Database** | Azure SQL / PostgreSQL Flexible Server | Amazon RDS / Aurora | Cloud SQL / AlloyDB | PostgreSQL, SQLite, MySQL |
| **NoSQL Database** | Azure Cosmos DB | Amazon DynamoDB | Firestore / Bigtable | MongoDB, Redis |
| **Cache** | Azure Cache for Redis | ElastiCache (Redis) | Memorystore | Redis (self-hosted) |
| **Search (Hybrid)** | Azure AI Search | Amazon OpenSearch | Vertex AI Search | Elasticsearch / OpenSearch |
| **Monitoring / Tracing** | Azure Monitor, App Insights | Amazon CloudWatch | Cloud Monitoring | LangSmith, Phoenix, Prometheus |
| **Content Safety** | Azure Content Safety | Bedrock Guardrails | Vertex AI Safety | Llama Guard (open source) |
| **Speech (STT/TTS)** | Azure AI Speech | Amazon Transcribe / Polly | Speech-to-Text / Text-to-Speech | Whisper (OpenAI, open source) |
| **Image Generation** | Azure DALL-E | Bedrock (Stability AI) | Imagen on Vertex AI | Stable Diffusion (local) |

---

### 18D. Pricing Snapshot — LLM Inference (per 1M tokens, Input / Output)

| Model | Azure / OpenAI | AWS Bedrock | GCP Vertex AI | Open Source |
|---|---|---|---|---|
| **GPT-5.5** | ~$15 / $60 | ❌ | ❌ | ❌ |
| **GPT-5.4** | $1.25 / $10 | ❌ | ❌ | ❌ |
| **GPT-5.4 Mini** | $0.75 / $4.50 | ❌ | ❌ | ❌ |
| **GPT-5.4 Nano** | $0.20 / $1.25 | ❌ | ❌ | ❌ |
| **GPT-4o** | $2.50 / $10 | ❌ | ❌ | ❌ |
| **Claude Opus 4.7** | ❌ | $5 / $25 | ~$5 / $25 | ❌ |
| **Claude Sonnet 4.6** | ❌ | $3 / $15 | ~$3 / $15 | ❌ |
| **Claude Haiku 4.5** | ❌ | $1 / $5 | ~$1 / $5 | ❌ |
| **Nova Pro** | ❌ | $0.80 / $3.20 | ❌ | ❌ |
| **Nova Lite** | ❌ | $0.06 / $0.24 | ❌ | ❌ |
| **Nova Micro** | ❌ | $0.035 / $0.14 | ❌ | ❌ |
| **Gemini 3.5 Flash** ⭐ | ❌ | ❌ | $1.50 / $9.00 | ❌ |
| **Gemini 3.1 Pro** | ❌ | ❌ | $2 / $12 · $4 / $18 (>200K) | ❌ |
| **Gemini 3.1 Flash** | ❌ | ❌ | $0.75 / $4.50 | ❌ |
| **Gemini 3.1 Flash-Lite** | ❌ | ❌ | $0.25 / $1.50 | ❌ |
| Gemini 2.0 Flash (prev gen) | ❌ | ❌ | $0.10 / $0.40 | ❌ |
| Gemini 1.5 Pro (prev gen) | ❌ | ❌ | $1.25 / $5 | ❌ |
| **Llama 3.3 70B** | Pay-as-you-go | $0.72 / $0.72 | ~$0.50 / $0.50 | **FREE** (self-hosted) |
| **Phi-4 (14B)** | Pay-as-you-go | ❌ | ❌ | **FREE** (Ollama/HF) |
| **Qwen 3.6 / Gemma 4** | ❌ | ❌ | Gemma: included | **FREE** (Ollama/HF) |

> **Cost-saving features across all cloud providers:**
> - **Batch inference**: 50% off (all platforms)
> - **Prompt caching**: up to 90% off repeated input (Anthropic / Azure)
> - **Spot / preemptible instances**: 60–80% cheaper for self-hosted inference

---

### 18E. When to Use Which Platform — Use Case Guide

| Use Case | Best Platform | Why |
|---|---|---|
| **Enterprise Microsoft stack (Teams, Office 365)** | Azure AI Foundry | Native AD, Compliance, Copilot integration |
| **Already on AWS (Lambda, S3, EC2)** | AWS Bedrock | IAM roles, VPC, S3 native, no extra auth |
| **Data-heavy workloads, BigQuery, GCS** | GCP Vertex AI | Native BigQuery ML, GCS, Dataflow |
| **Best reasoning model (Claude)** | AWS Bedrock or GCP | Claude only available via Bedrock/Vertex |
| **Cheapest production LLM** | AWS Bedrock (Nova Micro) | $0.035/$0.14 per 1M tokens |
| **Longest context (2M tokens)** | GCP Vertex AI | Gemini 3.1 Pro — 2M context, largest in production |
| **Local dev / no cloud costs** | Ollama + Chroma | Fully free, runs on laptop |
| **Privacy / on-prem / regulated data** | Ollama + self-hosted Qdrant | No data leaves your infrastructure |
| **Multilingual RAG** | BGE-M3 + any platform | Best multilingual open embedding |
| **Production RAG, team of 1–5** | Qdrant + Claude / GPT | Best latency, free self-host vector DB |
| **Enterprise RAG, full managed** | Azure AI Search + GPT | Hybrid search, managed, enterprise SLA |
| **Edge / mobile deployment** | Phi-4 or Gemma 4 E4B (Ollama) | Runs on consumer hardware |
| **Agentic coding / long-horizon tasks** | Claude Opus 4.8 (Bedrock) | Best for autonomous multi-step agents |
| **Image + text multimodal** | GPT-5.5 / Gemini 3.5 Flash / Nova Pro | Native vision support |
| **Real-time voice / video agent** | GCP Vertex AI (Gemini 3.1 Flash Live) | Ultra-low latency bidirectional audio+video |
| **AI video / image generation** | GCP Vertex AI (Imagen 4 / Veo 3.1) | Best-in-class media generation on cloud |
| **Cost prototyping** | Nova Micro / GPT-5.4 Nano / Haiku | Sub-$0.20 input per 1M tokens |
| **Fine-tuning your own model** | Azure AI Foundry / Vertex AI | Managed fine-tuning pipelines |

---

### 18F. One-Line Summary per Platform

| Platform | One-Line Summary |
|---|---|
| **Azure AI Foundry** | Best for Microsoft-ecosystem enterprises — GPT-5.x, Phi-4, managed RAG, compliance |
| **AWS Bedrock** | Best for AWS-native teams — multi-model (Claude + Nova + Llama), managed agents, cheapest models |
| **GCP Vertex AI** | Best for data-heavy GCP teams — Gemini 3.5 Flash (agentic), 3.1 Pro (2M ctx), Imagen 4, Veo 3.1 |
| **Ollama / HuggingFace** | Best for local dev, privacy, zero cost — all open-source models, full control |

---

## Sources

- [Anthropic Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Anthropic Context Windows Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [OpenAI GPT-5.4 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.4)
- [OpenAI GPT-5.4 Mini Docs](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
- [OpenAI GPT-5.4 Nano Docs](https://developers.openai.com/api/docs/models/gpt-5.4-nano)
- [OpenAI GPT-5.5 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.5)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [AWS Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [AWS Bedrock Supported Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Azure AI Foundry vs Azure OpenAI](https://az365.ai/blog/azure-ai-foundry-vs-azure-openai-2026-decision/)
- [Azure Foundry Models Catalog](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)
- [Azure OpenAI Pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/)
- [Google Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [GCP Vector Search & Embeddings](https://medium.com/google-cloud/making-sense-of-vector-search-and-embeddings-across-gcp-products-46cedad68934)
- [Best Embedding Models 2026 — Milvus Blog](https://milvus.io/blog/choose-embedding-model-rag-2026.md)
- [Open Source Embedding Models 2026](https://presenc.ai/research/best-open-weight-embedding-models-2026)
- [Vector Database Comparison 2026](https://reintech.io/blog/vector-database-comparison-2026-pinecone-weaviate-milvus-qdrant-chroma)
- [HNSW Internals — Pinecone](https://www.pinecone.io/learn/series/faiss/hnsw/)
- [HNSW Indexing Fundamentals — Qdrant](https://qdrant.tech/course/essentials/day-2/what-is-hnsw/)
- [Liquid AI LFM2.5-8B-A1B](https://www.liquid.ai/blog/lfm2-5-8b-a1b)
- [Qwen 3.6 Plus 1M Context](https://www.digitalapplied.com/blog/qwen-3-6-plus-1m-context-always-on-cot-guide)
- [Gemma 4 Developer Guide](https://lushbinary.com/blog/gemma-4-developer-guide-benchmarks-architecture-local-deployment-2026/)
- [Azure OpenAI Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)

- [Anthropic Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Anthropic Context Windows Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [OpenAI GPT-5.4 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.4)
- [OpenAI GPT-5.4 Mini Docs](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
- [OpenAI GPT-5.4 Nano Docs](https://developers.openai.com/api/docs/models/gpt-5.4-nano)
- [OpenAI GPT-5.5 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.5)
- [AWS Bedrock Supported Models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- [Azure AI Foundry vs Azure OpenAI](https://az365.ai/blog/azure-ai-foundry-vs-azure-openai-2026-decision/)
- [Azure Foundry Models Catalog](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)
- [Best Embedding Models 2026 — Milvus Blog](https://milvus.io/blog/choose-embedding-model-rag-2026.md)
- [Open Source Embedding Models 2026](https://presenc.ai/research/best-open-weight-embedding-models-2026)
- [Vector Database Comparison 2026](https://reintech.io/blog/vector-database-comparison-2026-pinecone-weaviate-milvus-qdrant-chroma)
- [HNSW Internals — Pinecone](https://www.pinecone.io/learn/series/faiss/hnsw/)
- [HNSW Indexing Fundamentals — Qdrant](https://qdrant.tech/course/essentials/day-2/what-is-hnsw/)
- [Liquid AI LFM2.5-8B-A1B](https://www.liquid.ai/blog/lfm2-5-8b-a1b)
- [Qwen 3.6 Plus 1M Context](https://www.digitalapplied.com/blog/qwen-3-6-plus-1m-context-always-on-cot-guide)
- [Gemma 4 Developer Guide](https://lushbinary.com/blog/gemma-4-developer-guide-benchmarks-architecture-local-deployment-2026/)
- [Azure OpenAI Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)
