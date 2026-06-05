# LLM Token Limits, Context Windows & API Rate Limits

> Note: Limits are subject to change. Always verify with the official provider docs for the latest values.

---

## What is a Token?

- 1 token ≈ 4 characters or 0.75 words in English
- "Hello world" = 2 tokens
- 1000 tokens ≈ 750 words ≈ ~1.5 pages of text
- Images, PDFs, and audio also consume tokens when passed to multimodal models

---

## 1. Anthropic Claude Models

| Model | Context Window (Input) | Max Output | Best Use Case |
|---|---|---|---|
| Claude Haiku 4.5 | 200K tokens | 8K tokens | Fast, cheap tasks, classification, summarization |
| Claude Sonnet 4.6 | 200K tokens | 64K tokens | Balanced — reasoning, RAG, coding, agents |
| Claude Opus 4.8 | 200K tokens | 32K tokens | Complex reasoning, long-form writing, research |
| Claude 3.7 Sonnet | 200K tokens | 64K tokens (extended thinking) | Deep multi-step reasoning |
| Claude 3.5 Haiku | 200K tokens | 8K tokens | High-speed, lightweight tasks |

**Notes:**
- All Claude models support 200K input context (≈ 150K words or ~500 pages)
- Extended thinking on Claude 3.7+ uses extra tokens internally — counts toward output limit
- Streaming is supported on all models

---

## 2. OpenAI / Azure OpenAI Models

| Model | Context Window (Input) | Max Output | Best Use Case |
|---|---|---|---|
| GPT-4o | 128K tokens | 16K tokens | Multimodal (text + image), RAG, agents |
| GPT-4o mini | 128K tokens | 16K tokens | Cheap, fast alternative to GPT-4o |
| GPT-4 Turbo | 128K tokens | 4K tokens | Long document analysis |
| GPT-4 | 8K / 32K tokens | 4K / 8K tokens | General reasoning (older, higher cost) |
| GPT-3.5 Turbo | 16K tokens | 4K tokens | Simple tasks, fast prototyping |
| o1 | 200K tokens | 100K tokens | Deep reasoning, math, code |
| o1-mini | 128K tokens | 65K tokens | Lightweight reasoning tasks |
| o3 | 200K tokens | 100K tokens | Advanced reasoning, research |
| o3-mini | 200K tokens | 65K tokens | Fast reasoning at lower cost |

**Azure OpenAI specific notes:**
- Models are deployed per region — not all models available in all Azure regions
- TPM (tokens per minute) quota is set at deployment level in Azure portal
- Default quota is often low (e.g. 10K–30K TPM) — must request increases via Azure portal
- Azure adds an extra network hop — slightly higher latency than OpenAI direct

---

## 3. Google Gemini Models

| Model | Context Window (Input) | Max Output | Best Use Case |
|---|---|---|---|
| Gemini 2.0 Flash | 1M tokens | 8K tokens | Fast, large-document processing |
| Gemini 1.5 Pro | 2M tokens | 8K tokens | Largest context available — full book analysis |
| Gemini 1.5 Flash | 1M tokens | 8K tokens | Fast and cheap large-context tasks |
| Gemini Ultra | 32K tokens | 8K tokens | High-capability general tasks |

**Notes:**
- Gemini 1.5 Pro's 2M context window is the largest publicly available as of mid-2025
- Great for ingesting entire codebases or books in one call
- Native multimodal: text, image, video, audio

---

## 4. Meta Llama (Open Source / Self-hosted)

| Model | Context Window | Max Output | Best Use Case |
|---|---|---|---|
| Llama 3.1 8B | 128K tokens | 8K tokens | Lightweight, local deployment |
| Llama 3.1 70B | 128K tokens | 8K tokens | Mid-tier local or cloud |
| Llama 3.1 405B | 128K tokens | 8K tokens | Best open-source quality |
| Llama 3.2 3B / 11B | 128K tokens | 8K tokens | Edge / mobile devices |
| Llama 3.3 70B | 128K tokens | 8K tokens | Near-GPT-4 quality at lower cost |

**Notes:**
- Free to run locally using Ollama, vLLM, or Hugging Face
- No API rate limits when self-hosted
- Quality varies significantly by model size

---

## 5. Mistral Models

| Model | Context Window | Max Output | Best Use Case |
|---|---|---|---|
| Mistral 7B | 32K tokens | 8K tokens | Lightweight, fast inference |
| Mistral Small | 32K tokens | 8K tokens | Simple tasks |
| Mistral Large | 128K tokens | 8K tokens | Complex reasoning, coding |
| Mixtral 8x7B | 32K tokens | 8K tokens | Open-source MoE, efficient |
| Codestral | 32K tokens | 8K tokens | Code generation |

---

## 6. API Rate Limits

### Anthropic (Claude API)

| Tier | Model | RPM (Requests/min) | TPM (Tokens/min) | TPD (Tokens/day) |
|---|---|---|---|---|
| Free | Haiku | 5 | 25,000 | 300,000 |
| Free | Sonnet | 5 | 40,000 | 300,000 |
| Free | Opus | 5 | 10,000 | 300,000 |
| Build (Paid) | Haiku | 1,000 | 100,000 | Unlimited |
| Build (Paid) | Sonnet | 1,000 | 80,000 | Unlimited |
| Build (Paid) | Opus | 500 | 40,000 | Unlimited |

- **429 error** = rate limit hit → implement exponential backoff
- Limits reset every 60 seconds

### OpenAI API

| Tier | RPM | TPM | Notes |
|---|---|---|---|
| Free | 3 | 40,000 | Very limited |
| Tier 1 ($5 spent) | 500 | 200,000 | Most common starting tier |
| Tier 2 ($50 spent) | 5,000 | 2,000,000 | Production-ready |
| Tier 3 ($100 spent) | 5,000 | 4,000,000 | High-volume apps |
| Tier 4 ($250 spent) | 10,000 | 10,000,000 | Enterprise |
| Tier 5 ($1000 spent) | 10,000 | 30,000,000 | Large scale |

### Azure OpenAI

| Default Quota | GPT-4o | GPT-4 Turbo | GPT-3.5 Turbo |
|---|---|---|---|
| TPM (default) | 30,000 | 10,000 | 120,000 |
| RPM (default) | 180 | 60 | 720 |

- Quotas are **per deployment**, not per account
- Increase via: Azure Portal → Your Resource → Quotas → Request increase
- Hard limits exist per region — may need to deploy to multiple regions for very high load

---

## 7. What Happens When You Hit a Limit

| Error Code | Meaning | Fix |
|---|---|---|
| 429 | Rate limit exceeded | Retry with exponential backoff |
| 400 | Prompt too long (context exceeded) | Reduce input, chunk documents |
| 500 | Server error | Retry after a short delay |
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

## 8. When to Use Input vs Output Tokens

### Input Tokens (Prompt)
- System prompt
- Conversation history (chat memory)
- Retrieved RAG documents
- User's question
- Tool/function definitions

**Tips:**
- Trim chat history to last N messages to avoid hitting context limit
- Compress RAG chunks — only send top-K most relevant
- Use caching (Anthropic prompt caching / Azure Semantic Cache) to reduce repeated input cost

### Output Tokens (Completion)
- The model's response
- Tool call arguments generated by the model
- Chain-of-thought / reasoning tokens (for o1/Claude extended thinking)

**Tips:**
- Set `max_tokens` to cap output and avoid runaway costs
- Structured output (JSON mode) tends to use fewer tokens than free-form prose
- Streaming reduces perceived latency for long outputs

---

## 9. Context Window Strategy for RAG Chatbots

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
- Leaves room for the model's output
- Models degrade in quality near the very end of their context window
- Prevents unexpected 400 errors from slight overflows

---

## 10. Cost-Aware Model Selection

| Task | Recommended Model | Why |
|---|---|---|
| Simple Q&A, classification | GPT-4o mini / Claude Haiku | Cheap and fast |
| RAG with moderate docs | GPT-4o / Claude Sonnet | Balanced quality/cost |
| Complex reasoning, coding | Claude Opus / o1 / o3 | Best accuracy |
| Very long documents (>100K tokens) | Gemini 1.5 Pro / Claude | Largest context |
| Real-time chat | GPT-4o mini / Haiku | Lowest latency |
| Local / private data | Llama 3.1 / Mistral (self-hosted) | No data leaves your infra |

---

## 11. Quick Reference — Context Limits at a Glance

```
2,000,000  tokens  →  Gemini 1.5 Pro          (~1,500,000 words)
  200,000  tokens  →  All Claude models        (~150,000 words)
  200,000  tokens  →  OpenAI o1 / o3           (~150,000 words)
  128,000  tokens  →  GPT-4o, GPT-4 Turbo      (~96,000 words)
  128,000  tokens  →  Llama 3.1, Mistral Large (~96,000 words)
   32,000  tokens  →  Mistral 7B               (~24,000 words)
   16,000  tokens  →  GPT-3.5 Turbo            (~12,000 words)
```
