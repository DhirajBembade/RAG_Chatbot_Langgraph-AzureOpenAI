# Production Deployment Guide — Security, Scalability, Architecture & Real-World Scenario

> End-to-end reference for taking a RAG / Agentic / MCP chatbot from laptop to production.
> Covers Azure, AWS, and GCP side-by-side.

---

## Part 1 — API Security Fundamentals

### The Golden Rules

```
1. NEVER hardcode secrets in code or commit them to Git
2. ALWAYS use HTTPS/TLS — never plain HTTP in production
3. ALWAYS authenticate every API request
4. ALWAYS validate and sanitize all inputs
5. ALWAYS apply least-privilege — give each service only what it needs
6. ROTATE secrets regularly
7. LOG everything, but never log raw credentials or PII
```

---

### Where Credentials Live (by Environment)

| Environment | Where to Store Secrets |
|---|---|
| **Local Dev** | `.env` file (add to `.gitignore`), never commit |
| **CI/CD Pipeline** | GitHub Actions Secrets, Azure DevOps Variable Groups |
| **Staging / Production** | Cloud secret store (Key Vault / Secrets Manager / Secret Manager) |
| **Container (Docker/K8s)** | Injected as environment variables from secret store at runtime |
| **Cloud VMs / Containers** | Managed Identity / IAM Role — no secrets at all, just permissions |

```bash
# .env (local only, NEVER commit)
AZURE_OPENAI_API_KEY=sk-...
AZURE_OPENAI_ENDPOINT=https://...
QDRANT_API_KEY=...
DB_PASSWORD=...
```

```python
# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

---

## Part 2 — Secret Management by Cloud

---

### Azure — Key Vault

**Service:** Azure Key Vault
**What it stores:** API keys, passwords, connection strings, certificates, encryption keys
**Best practice:** Use Managed Identity — the app authenticates to Key Vault with no stored secret

```bash
pip install azure-keyvault-secrets azure-identity
```

```python
from azure.identity import (
    DefaultAzureCredential,        # Tries: Managed Identity → CLI → env vars
    ManagedIdentityCredential,     # Production: VM/container identity
    ClientSecretCredential,        # Service principal (CI/CD)
)
from azure.keyvault.secrets import SecretClient

# In production: no key needed — uses Managed Identity
credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://my-vault.vault.azure.net/",
    credential=credential,
)

openai_key = client.get_secret("azure-openai-key").value
db_password = client.get_secret("postgres-password").value
```

**Setup flow:**
```
1. Create Key Vault in Azure Portal
2. Add secrets (API keys, passwords)
3. Assign "Key Vault Secrets User" role to your app's Managed Identity
4. App reads secrets at startup — no credentials in code or environment
```

---

### AWS — Secrets Manager & Parameter Store

**Services:**
- **Secrets Manager** — API keys, DB passwords, auto-rotation support
- **Systems Manager Parameter Store** — config values, cheaper than Secrets Manager
- **IAM Roles** — EC2/ECS/Lambda get permissions automatically, no stored key needed

```bash
pip install boto3
```

```python
import boto3
import json

# No credentials in code — uses IAM role attached to EC2/ECS/Lambda
client = boto3.client("secretsmanager", region_name="us-east-1")

secret = client.get_secret_value(SecretId="prod/rag-chatbot/openai")
secret_dict = json.loads(secret["SecretString"])

api_key = secret_dict["OPENAI_API_KEY"]
db_password = secret_dict["DB_PASSWORD"]
```

**IAM Role policy (least privilege):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue"],
    "Resource": "arn:aws:secretsmanager:us-east-1:123456789:secret:prod/rag-chatbot/*"
  }]
}
```

---

### GCP — Secret Manager

**Service:** GCP Secret Manager
**Auth:** Service Accounts + Workload Identity (no key files in production)

```bash
pip install google-cloud-secret-manager
```

```python
from google.cloud import secretmanager

# Workload Identity in GKE — no key file needed
client = secretmanager.SecretManagerServiceClient()

name = "projects/my-project/secrets/openai-api-key/versions/latest"
response = client.access_secret_version(request={"name": name})
api_key = response.payload.data.decode("UTF-8")
```

---

### Secrets Comparison Table

| | Azure Key Vault | AWS Secrets Manager | GCP Secret Manager |
|---|---|---|---|
| **Auth method** | Managed Identity | IAM Role | Workload Identity / Service Account |
| **Auto-rotation** | Yes (with Functions) | Yes (built-in for RDS) | Yes (with Cloud Functions) |
| **Pricing** | ~$0.03/10K operations | $0.40/secret/month | $0.06/10K operations |
| **Audit logs** | Azure Monitor | CloudTrail | Cloud Audit Logs |
| **Best for** | Azure-native apps | AWS-native apps | GCP-native apps |

---

## Part 3 — API Authentication & Authorization

### Layer 1 — API Gateway (First Line of Defense)

All external traffic hits the API Gateway **before** your application. It handles:
- API key validation
- Rate limiting (throttling)
- IP allowlisting / blocklisting
- SSL termination
- Request/response transformation

| | Azure | AWS | GCP |
|---|---|---|---|
| **Service** | Azure API Management (APIM) | Amazon API Gateway | Cloud Endpoints / Apigee |
| **Rate limiting** | Built-in policies | Usage plans + throttling | Quota policies |
| **Auth** | JWT, OAuth2, API keys | API keys, Cognito, IAM | API keys, Firebase Auth, IAM |
| **WAF** | Azure Front Door + WAF | AWS WAF | Cloud Armor |

---

### Layer 2 — Application Authentication

**FastAPI with JWT (production pattern):**

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt  # pip install PyJWT

app = FastAPI()
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/chat")
async def chat(request: ChatRequest, user_id: str = Depends(verify_token)):
    # user_id verified — proceed safely
    ...
```

**Azure AD / Entra ID (enterprise auth):**
```python
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=os.getenv("AZURE_CLIENT_ID"),
    tenant_id=os.getenv("AZURE_TENANT_ID"),
)

@app.get("/chat")
async def chat(user=Depends(azure_scheme)):
    # User is authenticated via Azure AD
    ...
```

---

### Layer 3 — Rate Limiting in FastAPI

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/chat")
@limiter.limit("10/minute")   # Max 10 requests per minute per IP
async def chat(request: Request, body: ChatRequest):
    ...
```

---

### Layer 4 — Network Security

```
Internet
    ↓
[Azure Front Door / AWS CloudFront / GCP Cloud CDN]  ← CDN + DDoS protection
    ↓
[WAF]  ← Block SQL injection, XSS, known attack patterns
    ↓
[API Gateway]  ← Auth, rate limiting, routing
    ↓
[Private VNet / VPC]  ← Your API cannot be reached from internet directly
    ↓
[FastAPI Container]  ← Only accessible within private network
    ↓
[Vector DB / LLM / DB]  ← Private endpoints, no public IP
```

**Key principle:** Your LLM API, vector DB, and database should have **no public IP**. Only the API Gateway / Load Balancer is internet-facing.

---

## Part 4 — Scalability Architecture

---

### What Needs to Scale in a RAG Chatbot

| Component | Bottleneck | Scaling Strategy |
|---|---|---|
| FastAPI app | CPU / memory under load | Horizontal scaling (more replicas) |
| LLM inference | Token throughput, latency | Use managed APIs (Azure/Bedrock) — they handle it |
| Vector search | Query throughput | Qdrant/Pinecone auto-scale, or read replicas |
| Embedding generation | Batch throughput | Async workers, batch API (50% cheaper) |
| Chat history DB | Read/write throughput | Redis for hot sessions, PostgreSQL with connection pooling |
| Document ingestion | Processing time | Async queue (Celery + Redis / SQS / Pub/Sub) |

---

### Azure — Scalability Services

```
[Azure API Management]          ← Rate limiting, auth, routing
        ↓
[Azure Container Apps]          ← Auto-scales 0→N replicas based on HTTP traffic or queue depth
        ↓
[Azure Cache for Redis]         ← Session cache, hot vector results, rate limit counters
        ↓
[Azure AI Search]               ← Managed vector + hybrid search, scales with replicas
        ↓
[Azure OpenAI]                  ← Managed LLM, scale by increasing TPM quota
        ↓
[Azure PostgreSQL Flexible]     ← Chat history, PgBouncer for connection pooling
        ↓
[Azure Blob Storage]            ← Unlimited document storage, CDN-backed
        ↓
[Azure Service Bus]             ← Async document ingestion queue
```

**Azure Container Apps scaling config:**
```yaml
# container-apps.yaml
scale:
  minReplicas: 1
  maxReplicas: 20
  rules:
    - name: http-scaling
      http:
        metadata:
          concurrentRequests: "10"   # Scale up when >10 concurrent requests per replica
    - name: queue-scaling
      custom:
        type: azure-servicebus
        metadata:
          queueName: doc-ingestion
          messageCount: "5"          # Scale up when >5 messages in queue
```

---

### AWS — Scalability Services

```
[Amazon API Gateway]            ← Rate limiting, auth, routing
        ↓
[AWS ECS Fargate / EKS]         ← Auto-scales containers, no server management
        ↓
[Amazon ElastiCache (Redis)]    ← Session cache, hot data
        ↓
[Amazon OpenSearch]             ← Managed vector + keyword search, scale data nodes
        ↓
[AWS Bedrock]                   ← Managed LLM, Provisioned Throughput for guaranteed TPM
        ↓
[Amazon RDS Aurora Serverless]  ← Auto-scales DB capacity 0→N ACUs
        ↓
[Amazon S3]                     ← Document storage, unlimited
        ↓
[Amazon SQS]                    ← Async document ingestion queue
```

**ECS Fargate auto-scaling:**
```json
{
  "scalingPolicy": {
    "targetTrackingScalingPolicyConfiguration": {
      "targetValue": 70.0,
      "predefinedMetricSpecification": {
        "predefinedMetricType": "ECSServiceAverageCPUUtilization"
      },
      "scaleOutCooldown": 60,
      "scaleInCooldown": 300
    }
  }
}
```

---

### GCP — Scalability Services

```
[Cloud Endpoints / Apigee]      ← Rate limiting, auth, routing
        ↓
[Cloud Run]                     ← Scales to 0, instant cold start, per-request billing
        ↓
[Memorystore (Redis)]           ← Session cache
        ↓
[Vertex AI Vector Search]       ← Managed vector search, scales independently
        ↓
[Vertex AI / Gemini API]        ← Managed LLM
        ↓
[Cloud SQL / AlloyDB]           ← Auto-storage increase, read replicas
        ↓
[Google Cloud Storage]          ← Document storage
        ↓
[Cloud Pub/Sub]                 ← Async document ingestion
```

**Cloud Run scaling config:**
```yaml
# cloud-run service
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "100"
        autoscaling.knative.dev/target: "80"   # Target 80 concurrent requests per instance
```

---

## Part 5 — Full Services Map for RAG / Agentic / MCP Workflows

---

### Every Service, Its Role, and Why It Matters

| Service Role | Azure | AWS | GCP | OSS Option | Why Important |
|---|---|---|---|---|---|
| **LLM** | Azure OpenAI (GPT-5.4) | Bedrock (Claude/Nova) | Vertex AI (Gemini 3.5) | Ollama (Llama/Qwen) | Core intelligence — generates answers |
| **Embedding** | text-embedding-3-small | Titan Embeddings V2 | text-embedding-004 | bge-m3 (local) | Converts text to vectors for search |
| **Vector Store** | Azure AI Search | OpenSearch / Aurora pgvector | Vertex AI Vector Search | Qdrant / Chroma | Semantic retrieval — the RAG backbone |
| **Document Storage** | Azure Blob Storage | Amazon S3 | Google Cloud Storage | MinIO | Stores raw PDFs, docs before processing |
| **Document Extraction** | Azure Doc Intelligence | Textract | Document AI | Docling / Unstructured | Parses PDFs with tables, layouts |
| **Chat History** | Cosmos DB / PostgreSQL | DynamoDB / RDS | Firestore / Cloud SQL | PostgreSQL + pgvector | Stores conversation turns per user |
| **Session Cache** | Azure Redis Cache | ElastiCache Redis | Memorystore | Redis (self-hosted) | Fast session lookup, hot vector results |
| **API Hosting** | Container Apps / AKS | ECS Fargate / EKS | Cloud Run / GKE | Docker + K8s | Runs your FastAPI chatbot |
| **API Gateway** | Azure API Management | Amazon API Gateway | Cloud Endpoints / Apigee | Kong / Traefik | Auth, rate limiting, routing |
| **Secret Management** | Key Vault | Secrets Manager | Secret Manager | HashiCorp Vault | Never hardcode credentials |
| **Content Safety** | Azure Content Safety | Bedrock Guardrails | Vertex AI Safety | Llama Guard / NeMo | Block harmful inputs/outputs |
| **Async Queue** | Service Bus | SQS / SNS | Pub/Sub | Celery + Redis | Document ingestion, background jobs |
| **Monitoring / Tracing** | Azure Monitor + App Insights | CloudWatch + X-Ray | Cloud Monitoring + Trace | Langfuse / Prometheus | Detect errors, latency, costs |
| **LLM Tracing** | Azure Monitor | CloudWatch | Cloud Trace | LangSmith / Langfuse | Trace every chain, agent, retrieval call |
| **Container Registry** | Azure Container Registry (ACR) | Amazon ECR | Google Artifact Registry | Docker Hub | Store Docker images |
| **CI/CD** | Azure DevOps / GitHub Actions | AWS CodePipeline / GitHub Actions | Cloud Build | GitHub Actions | Auto deploy on push |
| **CDN + WAF** | Azure Front Door | CloudFront + AWS WAF | Cloud CDN + Cloud Armor | Nginx + ModSecurity | DDoS protection, fast static delivery |
| **Identity / Auth** | Azure AD / Entra ID | AWS Cognito / IAM | Firebase Auth / IAM | Keycloak | Who can use the chatbot |

---

## Part 6 — Dockerizing Your Service

---

### Dockerfile — FastAPI RAG App

```dockerfile
# Multi-stage build — smaller final image
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim AS runtime

WORKDIR /app

# Non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Set ownership
RUN chown -R appuser:appgroup /app
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Uvicorn with multiple workers for production
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
# .dockerignore
__pycache__/
*.pyc
.env
.git
*.db
venv/
```

---

### docker-compose.yml — Local Dev Stack

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env                         # Local secrets — NOT committed to git
    depends_on:
      - qdrant
      - redis
      - postgres
    volumes:
      - ./:/app                      # Hot reload in dev

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: chatbot_db
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  qdrant_data:
  postgres_data:
```

---

### Deploying to Each Cloud

#### Azure — Container Apps

```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image rag-chatbot:latest .

# Deploy to Container Apps
az containerapp create \
  --name rag-chatbot-api \
  --resource-group my-rg \
  --image myregistry.azurecr.io/rag-chatbot:latest \
  --ingress external \
  --target-port 8000 \
  --min-replicas 1 \
  --max-replicas 20 \
  --secrets "openai-key=keyvaultref:https://my-vault.vault.azure.net/secrets/openai-key" \
  --env-vars "AZURE_OPENAI_API_KEY=secretref:openai-key"
```

#### AWS — ECS Fargate

```bash
# Push to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag rag-chatbot:latest <account>.dkr.ecr.us-east-1.amazonaws.com/rag-chatbot:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/rag-chatbot:latest

# ECS task uses IAM role — no secrets in env vars
# Secrets injected from Secrets Manager via task definition
```

#### GCP — Cloud Run

```bash
# Build and push to Artifact Registry
gcloud builds submit --tag gcr.io/my-project/rag-chatbot:latest

# Deploy to Cloud Run
gcloud run deploy rag-chatbot \
  --image gcr.io/my-project/rag-chatbot:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 1 \
  --max-instances 100 \
  --set-secrets "OPENAI_API_KEY=openai-api-key:latest"
```

---

## Part 7 — Monitoring

---

### What to Monitor in a RAG Chatbot

| Metric | Why | Alert Threshold |
|---|---|---|
| **API latency (p50, p95, p99)** | User experience — slow = bad | p95 > 5s |
| **Error rate (4xx, 5xx)** | Broken requests | > 1% errors |
| **LLM token usage** | Cost control | Spike > 2× baseline |
| **RAG retrieval quality** | Faithfulness/relevancy drift | Score < 0.7 |
| **Vector DB query latency** | Retrieval bottleneck | > 500ms |
| **Cache hit rate** | Redis efficiency | < 40% hit rate |
| **Queue depth** | Ingestion backlog | > 100 messages |
| **Container CPU/memory** | Scaling trigger | CPU > 70% |
| **Prompt injection attempts** | Security | Any detection |

---

### Azure Monitoring Stack

```python
# Application Insights — automatic tracing for FastAPI
pip install azure-monitor-opentelemetry

from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)
# All FastAPI requests, exceptions, dependencies auto-traced
```

```
Azure Monitor          — Infrastructure metrics (CPU, memory, network)
Application Insights   — App traces, request durations, exceptions, custom events
Log Analytics          — Centralized log queries (KQL)
Azure Alerts           — PagerDuty/email/Teams notifications on threshold breach
Azure Dashboards       — Custom metric dashboards
```

---

### AWS Monitoring Stack

```python
# CloudWatch custom metrics
import boto3

cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

cloudwatch.put_metric_data(
    Namespace="RAGChatbot",
    MetricData=[{
        "MetricName": "FaithfulnessScore",
        "Value": faithfulness_score,
        "Unit": "None",
    }]
)
```

```
CloudWatch Metrics     — Infrastructure + custom app metrics
CloudWatch Logs        — Centralized log storage and querying
AWS X-Ray              — Distributed tracing across services
CloudWatch Alarms      — Alerts to SNS → email/Slack/PagerDuty
CloudWatch Dashboards  — Metric visualization
```

---

### GCP Monitoring Stack

```python
# Cloud Trace — custom spans
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider

tracer_provider = TracerProvider()
tracer_provider.add_span_processor(
    BatchSpanProcessor(CloudTraceSpanExporter())
)
trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("rag-retrieval"):
    docs = retriever.invoke(query)
```

```
Cloud Monitoring       — Infrastructure metrics, uptime checks
Cloud Logging          — Centralized structured log storage
Cloud Trace            — Distributed tracing (OpenTelemetry native)
Cloud Error Reporting  — Automatic exception grouping and alerting
Alerting Policies      — Notifications to PagerDuty / email / Slack
```

---

### LLM-Specific Monitoring (All Clouds)

```python
# Langfuse — self-hostable LLM observability
from langfuse.callback import CallbackHandler

langfuse = CallbackHandler(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
)

# Every chain/agent call is automatically traced with:
# - Input / output
# - Token counts + cost
# - Latency per step
# - LLM model used
# - Retrieval results
result = rag_chain.invoke(input, config={"callbacks": [langfuse]})
```

---

## Part 8 — End-to-End Production Story

### Scenario: "IntelliHR" — Internal HR Policy Chatbot for a Financial Company

**Company:** FinCorp (5,000 employees)
**Goal:** Employees ask HR questions in natural language — the chatbot answers from 3,000+ policy PDFs
**Constraints:** GDPR compliant, all data stays in EU, no employee data to OpenAI servers

---

### Architecture Decision

```
Cloud: Azure (company already has Enterprise Agreement)
LLM: Azure OpenAI GPT-5.4 (data stays in Azure region)
Embedding: text-embedding-3-small (Azure OpenAI)
Vector Store: Azure AI Search (managed, hybrid search)
Auth: Azure AD / Entra ID (employees already have accounts)
Document Source: SharePoint → Azure Blob Storage
```

---

### System Architecture Diagram

```
[Employee Browser / Teams Bot]
          ↓  HTTPS
[Azure Front Door + WAF]           ← DDoS, SSL termination, CDN
          ↓
[Azure API Management]             ← Azure AD auth, rate limit (20 req/min/user)
          ↓
[Azure Container Apps — FastAPI]   ← Auto-scales 1→20 replicas
    ↓              ↓             ↓
[Azure Redis]  [Azure OpenAI]  [Azure AI Search]
(sessions)     (LLM + Embed)   (Vector + Hybrid Search)
                    ↓
              [Azure Content Safety]  ← Every input + output checked
                    ↓
         [Azure Cosmos DB]           ← Chat history per employee
                    ↓
           [Azure Key Vault]         ← All secrets (no hardcoding)
                    ↓
      [Azure Monitor + App Insights] ← All traces, metrics, alerts
                    ↓
        [Langfuse (self-hosted)]     ← LLM-specific traces, eval scores
```

---

### Step-by-Step Request Flow

```
Step 1 — Employee sends: "What is the maternity leave policy in Germany?"

Step 2 — Azure Front Door
  → TLS terminated
  → DDoS check passed
  → Routed to API Management

Step 3 — Azure API Management
  → Validates Azure AD JWT token
  → Checks rate limit: employee has 18/20 requests used this minute — OK
  → Forwards to Container Apps

Step 4 — FastAPI receives request
  → Parses JWT — extracts employee ID, department, country
  → Checks Redis cache: is this exact query cached? NO → proceed
  → Logs request start to Langfuse

Step 5 — Azure Content Safety (Input Check)
  → Scans message for harmful content
  → Checks for prompt injection patterns
  → Score: safe → proceed (if unsafe → return 400 with reason)

Step 6 — LangGraph Agent starts
  → State: { question, employee_country="DE", chat_history }
  → Router node decides: "HR policy question" → RAG path
    (if it were "general chat" → direct LLM path)
    (if it were "IT issue" → escalate to IT tool)

Step 7 — Retrieval (Multi-RAG)
  → MultiQueryRetriever generates 3 query variants:
      "maternity leave Germany"
      "parental leave policy German employees"
      "Germany family leave entitlement"
  → Azure AI Search hybrid query (vector + BM25) for each
  → EnsembleRetriever merges + deduplicates results
  → ContextualCompressionRetriever filters to only relevant sentences
  → Top 5 chunks returned with metadata (source PDF, page, last_updated)

Step 8 — LLM Generation
  → Prompt assembled:
      System: "You are IntelliHR assistant. Answer based ONLY on the context..."
      Context: [5 retrieved chunks]
      History: [last 3 turns]
      Human: "What is the maternity leave policy in Germany?"
  → Azure OpenAI GPT-5.4 called (streamed)
  → Tokens: 1,847 input + 312 output = 2,159 total

Step 9 — Azure Content Safety (Output Check)
  → Scans generated answer for harmful content → safe

Step 10 — Response
  → Streamed back to employee via SSE (Server-Sent Events)
  → Sources cited: "HR_Policy_DE_2025.pdf, page 14"
  → Cached in Redis for 1 hour (same query by any employee returns instantly)
  → Chat turn saved to Cosmos DB

Step 11 — Observability
  → Langfuse records: input, output, latency=1.8s, tokens=2159, cost=$0.003
  → App Insights records: HTTP 200, duration=1.8s, user=emp-12345
  → RAGAS score computed async: faithfulness=0.94, answer_relevancy=0.91
  → Azure Monitor checks: CPU 34%, 3/20 replicas active
```

---

### Document Ingestion Pipeline (Offline)

```
[SharePoint / HR Team uploads new PDF]
          ↓
[Azure Event Grid trigger]           ← Detects new blob in Azure Blob Storage
          ↓
[Azure Service Bus Queue]            ← Queues document for processing
          ↓
[Azure Container Apps — Worker]      ← Separate worker service, auto-scales
          ↓
[Azure AI Document Intelligence]     ← Extracts text, tables, layout
          ↓
[RecursiveCharacterTextSplitter]     ← chunk_size=1000, overlap=200
          ↓
[text-embedding-3-small]             ← Batch embedding (50% cheaper)
          ↓
[Azure AI Search]                    ← Upsert vectors + metadata
          ↓
[PostgreSQL — doc_registry table]    ← Record: file, chunk_count, ingested_at
          ↓
[Slack / Teams notification]         ← "HR_Policy_DE_2025.pdf indexed successfully"
```

---

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml

name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests + DeepEval LLM tests
        run: |
          pip install -r requirements.txt
          pytest tests/ --deepeval     # Fails if eval scores drop below threshold

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build and push to ACR
        run: |
          az acr build --registry ${{ secrets.ACR_NAME }} \
            --image rag-chatbot:${{ github.sha }} .

      - name: Deploy to Container Apps
        run: |
          az containerapp update \
            --name rag-chatbot-api \
            --resource-group prod-rg \
            --image ${{ secrets.ACR_NAME }}.azurecr.io/rag-chatbot:${{ github.sha }}
```

---

### Cost Breakdown (500 employees, 50 questions/day each)

```
Daily requests: 500 × 50 = 25,000
Avg tokens/request: 2,500 (input 2,000 + output 500)
Daily tokens: 62.5M

Azure OpenAI GPT-5.4:
  Input:  50M × $1.25/1M  = $62.50/day
  Output: 12.5M × $10/1M  = $125.00/day
  Subtotal LLM: ~$187/day = ~$5,600/month

text-embedding-3-small (queries):
  25K queries × 50 tokens avg = 1.25M tokens
  1.25M × $0.02/1M = $0.025/day ≈ negligible

Azure AI Search: ~$250/month (S1 tier, 3 replicas)
Azure Container Apps: ~$150/month (auto-scaled)
Azure Cosmos DB: ~$50/month
Azure Redis Cache: ~$50/month

Total: ~$6,100/month for 500 employees

With Redis caching (40% cache hit rate):
  LLM cost drops 40% → ~$3,700/month
```

---

### Production Checklist

```
Security:
  ✅ All secrets in Key Vault — no hardcoded credentials
  ✅ Managed Identity for all Azure service connections
  ✅ HTTPS enforced everywhere
  ✅ Azure AD auth on every endpoint
  ✅ Content safety on input AND output
  ✅ Rate limiting (20 req/min/user via APIM)
  ✅ Private endpoints for OpenAI, AI Search, Cosmos DB
  ✅ WAF rules active on Azure Front Door
  ✅ GDPR: EU region only, data residency confirmed

Reliability:
  ✅ Min 1 replica always running (no cold start)
  ✅ Max 20 replicas for peak load
  ✅ Redis cache to reduce LLM calls
  ✅ Retry with exponential backoff on LLM calls
  ✅ Graceful degradation if vector DB is slow
  ✅ Health check endpoint (/health)

Observability:
  ✅ Every request traced in App Insights
  ✅ Every LLM call traced in Langfuse
  ✅ RAGAS scores computed async for sample of requests
  ✅ DeepEval in CI — blocks deploy if quality drops
  ✅ Alerts on: error rate >1%, latency p95 >5s, cost spike >2x

Deployment:
  ✅ Docker multi-stage build (no dev dependencies in prod image)
  ✅ Non-root user in container
  ✅ CI/CD via GitHub Actions
  ✅ Blue/green deployment (no downtime on updates)
  ✅ Rollback plan (previous image tagged and ready)

Cost:
  ✅ Redis caching for repeated queries
  ✅ Batch embedding for document ingestion
  ✅ Auto-scale down to 1 replica overnight
  ✅ Token budget enforced (max_tokens=1000 on responses)
  ✅ Cost alerts in Azure Cost Management
```

---

## Part 9 — AWS & GCP Equivalents of the Same Architecture

### Same Architecture on AWS

```
[Employee] → [CloudFront + WAF] → [API Gateway] → [ECS Fargate FastAPI]
                                                          ↓
                                          [ElastiCache Redis] [Amazon OpenSearch]
                                                          ↓
                                           [AWS Bedrock Claude Sonnet 4.6]
                                                          ↓
                                           [Bedrock Guardrails] (content safety)
                                                          ↓
                                           [DynamoDB] (chat history)
                                           [Secrets Manager] (credentials)
                                           [CloudWatch + X-Ray] (monitoring)
                                           [SQS + Lambda] (doc ingestion)
                                           [Textract] (PDF extraction)
                                           [S3] (document storage)
```

### Same Architecture on GCP

```
[Employee] → [Cloud CDN + Cloud Armor] → [Apigee] → [Cloud Run FastAPI]
                                                           ↓
                                          [Memorystore Redis] [Vertex AI Vector Search]
                                                           ↓
                                          [Vertex AI Gemini 3.5 Flash]
                                                           ↓
                                          [Vertex AI Safety] (content safety)
                                                           ↓
                                          [Firestore] (chat history)
                                          [Secret Manager] (credentials)
                                          [Cloud Monitoring + Trace] (monitoring)
                                          [Pub/Sub + Cloud Functions] (doc ingestion)
                                          [Document AI] (PDF extraction)
                                          [GCS] (document storage)
```

---

## Summary — Service Selection Decision Tree

```
Starting a new project?
    ↓
Already on Azure? → Use Azure AI Foundry + Azure OpenAI + Azure AI Search
Already on AWS?   → Use Bedrock + OpenSearch + Fargate
Already on GCP?   → Use Vertex AI + Gemini + Cloud Run
New / no preference?
    → Need Claude?         → AWS Bedrock
    → Need GPT-5.x?        → Azure AI Foundry
    → Need 2M context?     → GCP Vertex AI (Gemini 3.1 Pro)
    → Privacy / on-prem?   → Self-hosted (Ollama + Qdrant + PostgreSQL)
    → Lowest cost MVP?     → GCP Cloud Run + Gemini 3.1 Flash-Lite ($0.25/1M)
```
