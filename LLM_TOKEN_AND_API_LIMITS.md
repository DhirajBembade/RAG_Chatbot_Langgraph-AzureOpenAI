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

## 3. Google Gemini Models

| Model | Context Window | Max Output | Best Use Case |
|---|---|---|---|
| Gemini 2.0 Flash | 1M tokens | 8K tokens | Fast, large-document processing |
| Gemini 1.5 Pro | 2M tokens | 8K tokens | Largest context — full book / codebase analysis |
| Gemini 1.5 Flash | 1M tokens | 8K tokens | Fast and cheap large-context tasks |

**Notes:**
- Gemini 1.5 Pro's **2M context** is among the largest publicly available
- Native multimodal: text, image, video, audio

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
2,000,000  tokens  →  Gemini 1.5 Pro                     (~1,500,000 words)
1,050,000  tokens  →  GPT-5.5, GPT-5.5 Pro               (~787,500 words)
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

## Sources

- [Anthropic Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview)
- [Anthropic Context Windows Docs](https://platform.claude.com/docs/en/build-with-claude/context-windows)
- [OpenAI GPT-5.4 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.4)
- [OpenAI GPT-5.4 Mini Model Docs](https://developers.openai.com/api/docs/models/gpt-5.4-mini)
- [OpenAI GPT-5.4 Nano Model Docs](https://developers.openai.com/api/docs/models/gpt-5.4-nano)
- [OpenAI GPT-5.5 Model Docs](https://developers.openai.com/api/docs/models/gpt-5.5)
- [Liquid AI LFM2.5-8B-A1B Blog](https://www.liquid.ai/blog/lfm2-5-8b-a1b)
- [Qwen 3.6 Plus — 1M Context Guide](https://www.digitalapplied.com/blog/qwen-3-6-plus-1m-context-always-on-cot-guide)
- [Gemma 4 Developer Guide](https://lushbinary.com/blog/gemma-4-developer-guide-benchmarks-architecture-local-deployment-2026/)
- [Azure OpenAI Quotas and Limits](https://learn.microsoft.com/en-us/azure/foundry/openai/quotas-limits)
