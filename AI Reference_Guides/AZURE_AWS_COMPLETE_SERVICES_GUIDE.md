# Azure & AWS Complete Services Guide
## AI · Agentic AI · MLOps · LLMOps · DevOps · Deployment · Monitoring

> Interview-ready reference. Every service explained: What / Why / When. Azure vs AWS side-by-side.

---

## Part 1 — Azure Services (Complete 2026)

---

### 1A. AI & Generative AI Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure AI Foundry** | Unified platform for building, deploying, managing AI apps and agents | Single place for model catalog, RAG, agents, evaluation, fine-tuning | Any new AI/LLM project on Azure |
| **Azure OpenAI Service** | Managed access to GPT-5.x, GPT-4o, DALL-E, Whisper via Azure | Data stays in your Azure region, enterprise compliance, SLA | When you need OpenAI models with GDPR/HIPAA/data residency |
| **Azure AI Search** | Managed vector + keyword hybrid search engine | Best-in-class retrieval for RAG — combines semantic and BM25 | RAG knowledge base, enterprise document search |
| **Azure AI Content Safety** | API that detects harmful content in text and images | Block violence, hate, self-harm, sexual content, PII | Every chatbot input/output in production |
| **Azure AI Document Intelligence** | Extract structured data from PDFs, forms, invoices, tables | Handles complex layouts, tables, handwriting — better than pypdf | Document-heavy RAG, invoice processing |
| **Azure AI Speech** | Speech-to-text, text-to-speech, real-time transcription | Production-grade STT/TTS with custom voice models | Voice bots, meeting transcription, accessibility |
| **Azure AI Vision** | Image analysis, OCR, object detection, face (restricted) | Analyze images in RAG or automation pipelines | Multimodal RAG, image classification, OCR |
| **Azure AI Language** | NLP — sentiment, entity extraction, summarization, classification | Pre-built NLP without building models | Entity extraction from documents, sentiment dashboards |
| **Azure AI Translator** | Real-time text + document translation (100+ languages) | Localize chatbot responses or documents | Multilingual RAG, global customer support |
| **Azure Bot Service** | Managed bot framework with channel integrations | Deploy chatbot to Teams, Slack, Web, WhatsApp from one place | Enterprise chatbots with multi-channel reach |
| **Azure AI Foundry Agents** | Build multi-step AI agents with tools, memory, knowledge | Native agent orchestration within Azure stack | Agentic workflows, autonomous task execution |
| **Azure Cognitive Search (legacy)** | Predecessor to AI Search | Still used in older deployments | Migrating to Azure AI Search |

---

### 1B. Compute Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure Container Apps** | Serverless container hosting with auto-scale | No K8s complexity, scales 0→N on HTTP/queue events | FastAPI, microservices, RAG APIs |
| **Azure Kubernetes Service (AKS)** | Managed Kubernetes cluster | Full control over container orchestration, stateful apps | Large-scale, complex microservice systems |
| **Azure Functions** | Serverless event-driven functions | Pay-per-execution, auto-scale, zero idle cost | Document ingestion triggers, async processing, webhooks |
| **Azure App Service** | Managed web app / API hosting (PaaS) | Simple deployment, built-in scaling, CI/CD integration | Simple REST APIs, web apps without container complexity |
| **Azure Container Instances (ACI)** | Single container, no orchestration | Fast spin-up for one-off jobs | Batch jobs, short-lived workers |
| **Azure Batch** | Large-scale parallel job processing | Process thousands of tasks in parallel | Bulk document embedding, data preprocessing |
| **Azure Virtual Machines** | IaaS — full OS control | Custom software, GPU workloads, legacy apps | Self-hosted models (Ollama), GPU inference |
| **Azure GPU VMs (NC/ND series)** | VMs with NVIDIA A100/H100 GPUs | Train or fine-tune LLMs | Model fine-tuning, high-performance inference |

---

### 1C. Storage Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure Blob Storage** | Object storage — files, PDFs, images, models | Unlimited, cheap, CDN-backed, event triggers | Document store for RAG ingestion pipeline |
| **Azure Data Lake Storage Gen2** | Hierarchical Blob with big data analytics support | Parquet/Delta Lake, used with Synapse/Databricks | ML feature stores, large-scale data pipelines |
| **Azure Files** | Managed NFS/SMB file share | Shared file system across containers | Model weights shared across replicas |
| **Azure Queue Storage** | Simple message queue | Lightweight job queue for async tasks | Simple ingestion triggers |
| **Azure Table Storage** | NoSQL key-value store, cheap | Massive simple lookups with low cost | Audit logs, simple metadata |

---

### 1D. Database Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure SQL Database** | Managed SQL Server (PaaS) | Relational data, ACID, enterprise SQL | Structured business data, reporting |
| **Azure PostgreSQL Flexible Server** | Managed PostgreSQL with pgvector | SQL + vector search in one DB, pgvector extension | Simpler RAG setups combining SQL + vectors |
| **Azure Cosmos DB** | Multi-model globally distributed NoSQL DB | Multi-region, 99.999% SLA, document/key-value/graph | Chat history, session storage, global apps |
| **Azure Cache for Redis** | Managed Redis in-memory cache | Sub-ms latency, session cache, rate limiting | Hot vector results, user sessions, rate limit counters |
| **Azure Synapse Analytics** | Unified data warehouse + big data analytics | SQL + Spark in one platform | ML feature engineering, large-scale data analysis |
| **Azure Databricks** | Apache Spark platform with ML capabilities | MLflow native, large-scale data + model training | ML pipelines, feature engineering, model training |
| **Azure Database for MySQL** | Managed MySQL | Open-source compatibility, simple apps | Web app backends, WordPress-style apps |

---

### 1E. Networking & Security

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure Virtual Network (VNet)** | Isolated private network | Private communication between services, no public internet | All production deployments — mandatory |
| **Azure Private Endpoint** | Private IP for PaaS services (OpenAI, Search, etc.) | Services have no public IP — traffic stays in VNet | Lock down OpenAI / AI Search to private access only |
| **Azure API Management (APIM)** | Full API gateway with policies | Auth, rate limiting, transformation, developer portal | Any public-facing API — first door into your system |
| **Azure Front Door** | Global CDN + WAF + load balancer | DDoS protection, global routing, SSL termination | Global apps needing low latency + DDoS protection |
| **Azure Application Gateway** | Regional L7 load balancer + WAF | Route traffic to backend containers with WAF rules | Single-region API with WAF, path-based routing |
| **Azure Key Vault** | Managed secrets, keys, certificates | No hardcoded credentials, secret rotation, audit logs | Every production app — store all secrets here |
| **Azure Entra ID (AD)** | Identity and access management | SSO, MFA, RBAC for users and services | Enterprise auth, Azure AD JWT tokens |
| **Azure DDoS Protection** | Network-layer DDoS mitigation | Absorbs volumetric attacks automatically | Production APIs exposed to internet |
| **Azure Firewall** | Cloud-native network firewall | Filter and log outbound traffic from VNet | Restrict what your containers can reach |

---

### 1F. Messaging & Integration

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure Service Bus** | Enterprise message queue with topics/subscriptions | Guaranteed delivery, dead-letter queue, ordering | Doc ingestion queue, async agent workflows |
| **Azure Event Grid** | Event routing — pub/sub at scale | React to blob uploads, resource changes, custom events | Trigger ingestion when new PDF uploaded to Blob |
| **Azure Event Hubs** | High-throughput event streaming (like Kafka) | Millions of events/sec, Kafka-compatible | Real-time log streaming, telemetry ingestion |
| **Azure Logic Apps** | Low-code workflow automation | Connect 400+ connectors without code | Automate SharePoint → Blob → ingestion pipeline |

---

### 1G. DevOps & MLOps Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure DevOps** | CI/CD pipelines, repos, boards, artifacts | End-to-end DevOps in Microsoft ecosystem | Enterprise teams standardized on Azure |
| **Azure Container Registry (ACR)** | Private Docker image registry | Store and version container images, geo-replicated | All containerized apps on Azure |
| **Azure Machine Learning (AML)** | Full ML platform — train, deploy, monitor models | Experiment tracking, pipeline automation, model registry | Classical ML + LLM fine-tuning pipelines |
| **MLflow on Azure ML** | Open-source experiment tracking integrated into AML | Track runs, params, metrics, model versions | ML experiment tracking |
| **Azure AI Foundry (LLMOps)** | Prompt management, evaluation, fine-tuning, deployment | LLMOps lifecycle in one place | Managing LLM applications through their lifecycle |

---

### 1H. Monitoring & Observability

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Azure Monitor** | Central platform for all Azure metrics and logs | Unified view of infrastructure health | Always-on for all Azure resources |
| **Application Insights** | APM — request tracing, exceptions, dependencies | End-to-end request tracing for apps | Every production app — trace every API call |
| **Log Analytics Workspace** | Centralized log store with KQL query language | Query logs across all services in one place | Debugging, compliance, security auditing |
| **Azure Alerts** | Notify on metric/log thresholds | PagerDuty / Teams / email when things go wrong | Error rate spikes, latency alerts, cost spikes |
| **Azure Cost Management** | Track and optimize cloud spending | Budget alerts, cost allocation, rightsizing | Always — prevent bill surprises |
| **Azure Policy** | Enforce compliance rules across resources | Block non-compliant configs before they deploy | Governance, compliance (GDPR, HIPAA) |

---

## Part 2 — AWS Services (Complete 2026)

---

### 2A. AI & Generative AI Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon Bedrock** | Managed access to Claude, Nova, Llama, Mistral, Cohere, Titan | Multi-model via one API, data stays in AWS | Any LLM project on AWS — primary choice |
| **Bedrock Knowledge Bases** | Managed RAG — auto-ingest, chunk, embed, store, retrieve | Build RAG in minutes without custom pipeline | Quick RAG prototypes, managed knowledge bases |
| **Bedrock Agents** | Build multi-step agents with tools, Lambda actions | Native agentic AI within AWS — no orchestration code | Production agents that call AWS services |
| **Bedrock Guardrails** | Content filtering, PII, topic denial, grounding check | Safety layer applied on every Bedrock model call | Every production Bedrock deployment |
| **Bedrock Model Evaluation** | Run automated evals on your Bedrock models | Compare model versions, detect quality drift | Before deploying new model version |
| **Amazon Bedrock Flows** | Visual drag-and-drop LLM pipeline builder | No-code RAG and agent workflow construction | Rapid prototyping, non-developer teams |
| **Amazon SageMaker** | Full ML platform — training, deployment, MLOps | End-to-end ML lifecycle on AWS | Classical ML, custom LLM fine-tuning, MLOps |
| **SageMaker JumpStart** | Pre-built ML solutions and foundation models | Deploy Llama/Falcon/etc. in one click | Self-hosted open models on AWS |
| **Amazon Q Business** | Enterprise AI assistant powered by your company data | Managed RAG over your internal documents, no code | Non-technical companies wanting RAG fast |
| **Amazon Q Developer** | AI coding assistant for AWS services | Write, debug, explain code in AWS console/IDE | Developer productivity on AWS |
| **Amazon Kendra** | Intelligent enterprise search | NLP-powered search over internal documents | Enterprise document search (non-vector) |
| **Amazon Comprehend** | NLP — entities, sentiment, key phrases, PII | Pre-built NLP without custom models | PII detection, sentiment analysis in pipelines |
| **Amazon Textract** | Extract text, tables, forms from documents | Better than OCR for structured document extraction | Invoice processing, form digitization, PDF tables |
| **Amazon Rekognition** | Image and video analysis, face detection, labels | Analyze images without building CV models | Image safety checks, content moderation |
| **Amazon Polly** | Text-to-speech (TTS) with neural voices | Natural-sounding voice output for chatbots | Voice bots, accessibility, audio content |
| **Amazon Transcribe** | Speech-to-text (STT), real-time + batch | Transcribe calls, meetings, voice input | Call analytics, voice chatbots, captions |
| **Amazon Lex** | Build conversational chatbots with NLU | Managed intent recognition, slot filling, dialog | Rule-based chatbots, IVR systems |
| **Amazon Translate** | Neural machine translation (75+ languages) | Localize content at scale | Multilingual customer support, document translation |
| **Amazon Personalize** | Real-time ML-powered recommendations | Personalized content/product recs without ML expertise | E-commerce, content streaming recommendations |

---

### 2B. Compute Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon EC2** | Virtual machines — full OS control | Any workload, GPU instances, full flexibility | Self-hosted models, legacy apps, custom configs |
| **AWS Lambda** | Serverless event-driven functions | Zero idle cost, scales instantly, pay-per-ms | Webhooks, async triggers, document processing |
| **Amazon ECS (Fargate)** | Managed containers without server management | No cluster management, scales automatically | FastAPI containers, microservices |
| **Amazon EKS** | Managed Kubernetes | Full K8s control, community ecosystem | Complex microservices, large-scale container orchestration |
| **AWS App Runner** | Fully managed container deployment from source/image | Simplest way to deploy a container — zero config | Simple APIs, quick prototypes |
| **AWS Batch** | Managed batch computing | Run thousands of parallel jobs | Bulk embedding, model training jobs |
| **EC2 GPU Instances (P4, P5, G6)** | NVIDIA A100/H100 GPU VMs | Train and fine-tune LLMs | Model fine-tuning, high-throughput inference |

---

### 2C. Storage Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon S3** | Object storage — unlimited, 11 nines durability | Cheapest durable storage, event triggers, versioning | All document storage for RAG ingestion |
| **Amazon EFS** | Managed NFS file system | Shared storage across EC2/ECS/Lambda | Shared model weights, shared configs |
| **Amazon EBS** | Block storage for EC2 | High-performance disk for VMs | Database storage, EC2-attached disks |
| **S3 Glacier** | Long-term archival storage | Extremely cheap — $0.004/GB/month | Compliance archives, old log retention |
| **AWS Snow Family** | Physical data transfer devices | Move petabytes when network is too slow | One-time large data migrations |

---

### 2D. Database Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon RDS** | Managed relational DB (PostgreSQL, MySQL, SQL Server) | No DB admin, automated backups, read replicas | Chat history, business data |
| **Amazon Aurora** | High-performance managed MySQL/PostgreSQL | 5× faster than MySQL, auto-scaling storage | High-traffic production databases |
| **Aurora Serverless v2** | Aurora that scales to zero | Pay only for what you use, no provisioning | Variable workloads, dev/staging |
| **Amazon DynamoDB** | Serverless NoSQL key-value document DB | Single-digit ms latency, infinite scale | Chat history, session state, high-write workloads |
| **Amazon ElastiCache** | Managed Redis or Memcached | Sub-ms caching, session store | Hot vector cache, rate limit counters, sessions |
| **Amazon MemoryDB** | Redis-compatible with durability | Redis speed + durability (like Redis + AOF) | When you need Redis with persistence |
| **Amazon OpenSearch** | Managed Elasticsearch + vector search | Hybrid search (BM25 + vector), Kibana dashboards | RAG vector store, log analytics, full-text search |
| **Amazon Redshift** | Managed data warehouse | Petabyte-scale analytics, columnar storage | ML feature stores, business intelligence |
| **Amazon Neptune** | Managed graph database | Relationships, knowledge graphs | Knowledge graph RAG, fraud detection |
| **Amazon DocumentDB** | MongoDB-compatible managed DB | Migrate MongoDB workloads to AWS | Document store with MongoDB API |

---

### 2E. Networking & Security

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon VPC** | Isolated private network | All production resources live in private subnets | Every production deployment — mandatory |
| **VPC PrivateLink** | Private connectivity to AWS services | Bedrock, S3, DynamoDB with no public internet hop | Lock down all AWS service calls to private network |
| **Amazon API Gateway** | REST + WebSocket + HTTP API management | Auth, throttling, routing, API keys | All public-facing APIs |
| **Amazon CloudFront** | Global CDN with edge caching | Low latency globally, DDoS absorption at edge | Public APIs, static assets, streaming |
| **AWS WAF** | Web Application Firewall | Block SQLi, XSS, bot traffic, custom rules | Any public-facing API or web app |
| **AWS Shield** | DDoS protection (Standard = free, Advanced = paid) | Automatically mitigate large DDoS attacks | Standard: always on; Advanced: mission-critical apps |
| **AWS Secrets Manager** | Manage secrets with auto-rotation | Rotate RDS passwords automatically, no hardcoded secrets | All credentials — API keys, DB passwords |
| **AWS Systems Manager Parameter Store** | Config and secret storage (cheaper) | Free tier, good for non-sensitive config values | App config, feature flags |
| **AWS IAM** | Identity and access management | Least-privilege permissions for every service | Everything — every resource needs an IAM policy |
| **AWS KMS** | Key Management Service | Encrypt data at rest, control encryption keys | Encrypting S3, RDS, DynamoDB data |
| **AWS Cognito** | User authentication (sign-up, sign-in, MFA) | Managed auth for your app users | Customer-facing apps needing login/auth |

---

### 2F. Messaging & Integration

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon SQS** | Simple managed message queue | Decouple services, guaranteed delivery, dead-letter queue | Doc ingestion queue, async agent tasks |
| **Amazon SNS** | Pub/sub notification service | Fan-out messages to multiple subscribers | Notifications to email/Lambda/SQS on events |
| **Amazon EventBridge** | Serverless event bus (like Azure Event Grid) | Route events from AWS services, SaaS, custom apps | Trigger ingestion on S3 upload, cross-service events |
| **Amazon Kinesis** | Real-time data streaming (like Kafka) | Process millions of events/sec in real time | Real-time log streaming, clickstream analysis |
| **AWS Step Functions** | Visual serverless workflow orchestration | Coordinate Lambda functions with state and retry | Multi-step async workflows, document processing pipelines |
| **Amazon MQ** | Managed ActiveMQ/RabbitMQ | Lift-and-shift message broker workloads | Migrating on-prem RabbitMQ/ActiveMQ |

---

### 2G. DevOps Services

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **AWS CodePipeline** | Fully managed CI/CD pipeline | Automate build → test → deploy on AWS | AWS-native CI/CD |
| **AWS CodeBuild** | Managed build service | Run tests, build Docker images, no server needed | Build step in CodePipeline |
| **AWS CodeDeploy** | Automated deployment to EC2/ECS/Lambda | Blue/green, canary, rolling deployments | Zero-downtime deployments |
| **Amazon ECR** | Private Docker container registry | Store and version container images, IAM-integrated | All containerized AWS apps |
| **AWS CloudFormation** | Infrastructure as Code (IaC) with JSON/YAML | Reproducible, version-controlled infrastructure | Consistent infrastructure across environments |
| **AWS CDK** | Define CloudFormation with Python/TypeScript | Developer-friendly IaC with real programming languages | Modern IaC, ML platform provisioning |
| **AWS Systems Manager** | Operational management across EC2 fleet | Patch management, run commands, parameter store | EC2 fleet management, config management |

---

### 2H. Monitoring & Observability

| Service | What It Is | Why Use It | When to Use |
|---|---|---|---|
| **Amazon CloudWatch** | Metrics, logs, alarms, dashboards for all AWS | Central observability for every AWS service | Always-on — every AWS resource |
| **CloudWatch Logs Insights** | Query logs with a SQL-like language | Find patterns, errors, latency in logs fast | Debugging production issues |
| **AWS X-Ray** | Distributed tracing across services | See the full call chain (API → Lambda → DynamoDB) | Microservices latency debugging |
| **AWS CloudTrail** | Audit log of every API call to AWS | Security compliance, "who did what when" | Security auditing, compliance (SOC2, HIPAA) |
| **Amazon GuardDuty** | ML-based threat detection | Detect crypto mining, unusual API calls, credential theft | Security monitoring — always on |
| **AWS Health Dashboard** | AWS service outage and health notifications | Know when AWS itself has issues before your users do | Operational awareness |
| **Amazon DevOps Guru** | ML-powered anomaly detection for ops | Proactively surface operational issues | Proactive reliability engineering |

---

## Part 3 — Comparative Table: Azure vs AWS

### AI & Generative AI

| Capability | Azure | AWS |
|---|---|---|
| **LLM Platform** | Azure AI Foundry / Azure OpenAI | Amazon Bedrock |
| **Available LLMs** | GPT-5.x, Phi-4, Llama, Mistral | Claude, Nova, Llama, Mistral, Cohere, Titan |
| **Best Unique LLM** | GPT-5.5 / GPT-5.4 (OpenAI exclusive) | Claude Opus 4.8 (Anthropic) |
| **Managed RAG** | Azure AI Search + Prompt Flow | Bedrock Knowledge Bases |
| **Managed Agents** | Azure AI Foundry Agents | Bedrock Agents |
| **Content Safety** | Azure AI Content Safety | Bedrock Guardrails |
| **Document Extraction** | Azure AI Document Intelligence | Amazon Textract |
| **Speech STT/TTS** | Azure AI Speech | Amazon Transcribe / Polly |
| **Image Analysis** | Azure AI Vision | Amazon Rekognition |
| **NLP Pre-built** | Azure AI Language | Amazon Comprehend |
| **Translation** | Azure AI Translator | Amazon Translate |
| **Enterprise Search** | Azure AI Search | Amazon Kendra / OpenSearch |
| **LLM Eval** | Azure AI Evaluation SDK | Bedrock Model Evaluation |
| **Fine-tuning** | Azure AI Foundry fine-tune | SageMaker / Bedrock fine-tune |

---

### Compute

| Capability | Azure | AWS |
|---|---|---|
| **Serverless Containers** | Azure Container Apps | AWS App Runner / ECS Fargate |
| **Kubernetes** | AKS | EKS |
| **Serverless Functions** | Azure Functions | AWS Lambda |
| **PaaS Web Hosting** | Azure App Service | AWS Elastic Beanstalk |
| **VMs** | Azure Virtual Machines | Amazon EC2 |
| **GPU VMs** | NC/ND series (A100, H100) | P4, P5, G6 (A100, H100) |
| **Batch Jobs** | Azure Batch | AWS Batch |

---

### Storage & Databases

| Capability | Azure | AWS |
|---|---|---|
| **Object Storage** | Azure Blob Storage | Amazon S3 |
| **Vector + Search** | Azure AI Search | Amazon OpenSearch |
| **Relational DB** | Azure PostgreSQL / SQL Database | Amazon RDS / Aurora |
| **NoSQL Document** | Azure Cosmos DB | Amazon DynamoDB |
| **In-Memory Cache** | Azure Redis Cache | Amazon ElastiCache |
| **Data Warehouse** | Azure Synapse Analytics | Amazon Redshift |
| **Big Data + ML** | Azure Databricks | Amazon EMR / Glue |
| **Graph DB** | Cosmos DB (Gremlin API) | Amazon Neptune |

---

### Security & Networking

| Capability | Azure | AWS |
|---|---|---|
| **Private Network** | Azure VNet | Amazon VPC |
| **Private Service Access** | Azure Private Endpoint | AWS PrivateLink |
| **API Gateway** | Azure API Management | Amazon API Gateway |
| **CDN + WAF** | Azure Front Door | Amazon CloudFront + WAF |
| **Identity / Auth** | Azure Entra ID (AD) | AWS IAM + Cognito |
| **Secret Management** | Azure Key Vault | AWS Secrets Manager |
| **Encryption Keys** | Azure Key Vault (HSM) | AWS KMS |
| **DDoS Protection** | Azure DDoS Protection | AWS Shield |
| **Network Firewall** | Azure Firewall | AWS Network Firewall |
| **Threat Detection** | Microsoft Defender for Cloud | Amazon GuardDuty |

---

### Messaging & Integration

| Capability | Azure | AWS |
|---|---|---|
| **Message Queue** | Azure Service Bus | Amazon SQS |
| **Pub/Sub Events** | Azure Event Grid | Amazon EventBridge / SNS |
| **Streaming** | Azure Event Hubs | Amazon Kinesis |
| **Workflow Orchestration** | Azure Logic Apps | AWS Step Functions |
| **Kafka-compatible** | Azure Event Hubs (Kafka protocol) | Amazon MSK (managed Kafka) |

---

### DevOps & CI/CD

| Capability | Azure | AWS |
|---|---|---|
| **CI/CD Pipeline** | Azure DevOps Pipelines | AWS CodePipeline |
| **Build Service** | Azure DevOps Build | AWS CodeBuild |
| **Container Registry** | Azure Container Registry (ACR) | Amazon ECR |
| **IaC (YAML)** | ARM Templates / Bicep | AWS CloudFormation |
| **IaC (Code)** | Azure CDK / Terraform | AWS CDK / Terraform |
| **GitOps** | GitHub Actions + Azure | GitHub Actions + AWS |

---

### Monitoring & Observability

| Capability | Azure | AWS |
|---|---|---|
| **Metrics & Dashboards** | Azure Monitor | Amazon CloudWatch |
| **APM Tracing** | Application Insights | AWS X-Ray |
| **Log Management** | Log Analytics (KQL) | CloudWatch Logs Insights |
| **Security Audit Logs** | Azure Activity Log | AWS CloudTrail |
| **Threat Detection** | Defender for Cloud | Amazon GuardDuty |
| **Cost Management** | Azure Cost Management | AWS Cost Explorer |

---

## Part 4 — Agentic AI on Azure and AWS

---

### What is Agentic AI?

Agentic AI refers to AI systems that can **plan, reason, take actions, use tools, and operate autonomously over multiple steps** — not just answer a single question, but complete a goal.

```
Traditional chatbot: Question → Answer (one shot)

Agentic AI: Goal → Plan → Step 1 → Tool call → Observe → Step 2 → ...→ Done
```

**Key agent components:**
| Component | Role |
|---|---|
| **LLM** | Reasoning engine — decides what to do next |
| **Tools** | Actions the agent can take (search, code, DB query, API call) |
| **Memory** | Remembers previous steps and results |
| **Planner** | Breaks goal into sub-steps |
| **Orchestrator** | Controls the agent loop (LangGraph, Bedrock Agents, etc.) |

---

### Agentic AI on Azure

| Service | Role in Agentic AI |
|---|---|
| **Azure AI Foundry Agents** | Native agent builder — connect tools, OpenAPI, Azure functions |
| **Azure OpenAI (GPT-5.4)** | Core reasoning model for agents |
| **Azure AI Search** | Knowledge retrieval tool for agents |
| **Azure Functions** | Tool execution — agents call Lambda-like functions |
| **Azure Logic Apps** | Connect agents to 400+ business systems (SAP, Salesforce, etc.) |
| **Azure Service Bus** | Async agent task queue — long-running agent jobs |
| **Azure Cosmos DB** | Agent memory / state persistence |
| **Azure Container Apps** | Host LangGraph agents as scalable APIs |
| **Azure Key Vault** | Secrets for tools the agent calls |
| **Application Insights** | Trace every agent step, tool call, LLM invocation |

**Azure Foundry Agent pattern:**
```python
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

client = AIProjectClient(
    endpoint="https://<project>.api.azureml.ms",
    credential=DefaultAzureCredential(),
)

# Create agent with tools
agent = client.agents.create_agent(
    model="gpt-5.4",
    name="hr-policy-agent",
    instructions="You are an HR assistant. Use the search tool to find policies.",
    tools=[{"type": "azure_ai_search"}],  # Built-in Azure AI Search tool
)

# Run agent
thread = client.agents.create_thread()
client.agents.create_message(thread.id, role="user", content="What is the parental leave policy?")
run = client.agents.create_and_process_run(thread.id, agent_id=agent.id)
```

---

### Agentic AI on AWS

| Service | Role in Agentic AI |
|---|---|
| **Amazon Bedrock Agents** | Native agent builder — connect Knowledge Bases, Lambda tools |
| **Bedrock Knowledge Bases** | RAG retrieval tool for agents |
| **AWS Lambda** | Tool execution — agents invoke Lambda functions as actions |
| **AWS Step Functions** | Orchestrate multi-agent workflows with state and retry |
| **Amazon DynamoDB** | Agent memory / conversation state |
| **Amazon SQS** | Queue long-running agent jobs |
| **Amazon S3** | Document store agents retrieve from |
| **AWS Secrets Manager** | Secrets for tool APIs the agent calls |
| **Amazon CloudWatch** | Trace and monitor every agent invocation |
| **Bedrock Guardrails** | Safety on every agent input/output |

**Bedrock Agent + Lambda tool pattern:**
```python
import boto3
import json

bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

response = bedrock_agent_runtime.invoke_agent(
    agentId="<agent-id>",
    agentAliasId="<alias-id>",
    sessionId="user-123-session",
    inputText="What is the Q3 sales forecast?",
)

# Stream agent response and tool calls
for event in response["completion"]:
    if "chunk" in event:
        print(event["chunk"]["bytes"].decode(), end="", flush=True)
```

---

## Part 5 — ML / MLOps

### What is MLOps?

MLOps is the practice of applying **DevOps principles to Machine Learning** — automating the full lifecycle of a model: data prep → training → evaluation → deployment → monitoring → retraining.

```
Data → Feature Engineering → Training → Evaluation → Model Registry
                                                           ↓
                                               Deploy → Serve → Monitor
                                                                   ↓
                                                         Drift Detected → Retrain
```

---

### MLOps on Azure — Azure Machine Learning (AML)

| AML Component | What It Does |
|---|---|
| **Workspaces** | Top-level resource — contains all experiments, models, endpoints |
| **Compute Clusters** | Auto-scaling CPU/GPU clusters for training jobs |
| **Compute Instances** | Dev notebooks with pre-installed ML packages |
| **Datasets** | Versioned, registered data sources (Azure Blob / ADLS) |
| **Experiments & Runs** | Track training runs with params, metrics, artifacts |
| **Pipelines** | Automate multi-step ML workflows (data → train → eval → register) |
| **Model Registry** | Version, tag, and manage trained models |
| **Environments** | Docker-based environments with Python packages — reproducible |
| **Endpoints (Online)** | Real-time inference REST endpoint (Kubernetes or managed) |
| **Endpoints (Batch)** | Async batch scoring for large datasets |
| **MLflow Integration** | Native MLflow tracking built into AML |
| **Responsible AI Dashboard** | Fairness, explainability, error analysis for models |
| **Data Drift Monitor** | Detect when production data drifts from training data |

**Azure ML training job:**
```python
from azure.ai.ml import MLClient, command
from azure.ai.ml.entities import Environment
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id="<sub>",
    resource_group_name="<rg>",
    workspace_name="<workspace>",
)

job = command(
    code="./src",                        # Training script folder
    command="python train.py --lr 0.001 --epochs 10",
    environment="AzureML-sklearn-1.0:1",
    compute="gpu-cluster",
    experiment_name="rag-embedding-finetune",
)
returned_job = ml_client.jobs.create_or_update(job)
```

---

### MLOps on AWS — Amazon SageMaker

| SageMaker Component | What It Does |
|---|---|
| **Studio** | Web-based IDE for data science and ML |
| **Notebooks** | Managed Jupyter notebooks |
| **Training Jobs** | Distributed training on managed instances |
| **Processing Jobs** | Data preprocessing, feature engineering |
| **Pipelines** | MLOps workflows: data → process → train → evaluate → register |
| **Model Registry** | Version and approve models before deployment |
| **Feature Store** | Centralized feature repository for training + inference |
| **Experiments** | Track and compare training runs (like MLflow) |
| **Model Monitor** | Detect data drift and model quality degradation in production |
| **Endpoints (Real-time)** | REST inference API with auto-scaling |
| **Batch Transform** | Async scoring for large datasets |
| **JumpStart** | One-click deploy of Llama, Falcon, Stable Diffusion |
| **Clarify** | Bias detection and model explainability |
| **Ground Truth** | Human data labeling for training datasets |

**SageMaker training job (Python SDK):**
```python
import sagemaker
from sagemaker.pytorch import PyTorch

estimator = PyTorch(
    entry_point="train.py",
    source_dir="./src",
    role=sagemaker.get_execution_role(),
    instance_count=1,
    instance_type="ml.g5.4xlarge",  # GPU instance
    framework_version="2.1",
    py_version="py310",
    hyperparameters={"lr": 0.001, "epochs": 10},
)
estimator.fit({"training": "s3://my-bucket/data/"})
```

---

### MLOps Comparison: Azure ML vs SageMaker

| Capability | Azure ML | AWS SageMaker |
|---|---|---|
| **Experiment Tracking** | MLflow native | SageMaker Experiments + MLflow |
| **Pipeline Automation** | AML Pipelines | SageMaker Pipelines |
| **Model Registry** | AML Model Registry | SageMaker Model Registry |
| **Feature Store** | AML + Databricks | SageMaker Feature Store |
| **Data Labeling** | Azure ML Data Labeling | SageMaker Ground Truth |
| **Drift Detection** | AML Data Drift Monitor | SageMaker Model Monitor |
| **Bias/Fairness** | Responsible AI Dashboard | SageMaker Clarify |
| **Real-time Inference** | AML Managed Online Endpoint | SageMaker Real-time Endpoint |
| **Batch Inference** | AML Batch Endpoint | SageMaker Batch Transform |
| **GPU Training** | NC/ND VMs | ml.g5 / ml.p4 instances |
| **Open Model Deploy** | AML + AI Foundry | SageMaker JumpStart |

---

## Part 6 — LLMOps

### What is LLMOps?

LLMOps is MLOps **specifically for Large Language Models**. LLMs have unique challenges that traditional MLOps doesn't address:

| Challenge | Why LLMs Are Different |
|---|---|
| **Prompt engineering** | Prompts are part of the model — need versioning and testing |
| **Evaluation** | No single accuracy metric — need faithfulness, relevancy, safety |
| **Hallucinations** | LLMs confidently generate wrong answers |
| **Context management** | Token windows, chunking, retrieval quality all affect output |
| **Cost unpredictability** | Token-based billing can spike unexpectedly |
| **Model versioning** | Model updates (gpt-4o → gpt-5.4) can change behavior |

---

### LLMOps Lifecycle

```
1. DEVELOP     Prompt engineering, RAG pipeline design, tool selection
      ↓
2. EVALUATE    RAGAS / DeepEval — measure faithfulness, relevancy, safety
      ↓
3. DEPLOY      Container → API Gateway → monitoring enabled
      ↓
4. MONITOR     Trace every LLM call, track cost, measure quality on samples
      ↓
5. IMPROVE     Update prompts, change chunking, swap models, fine-tune
      ↓
6. GATE        CI/CD eval score gate — block deploy if quality drops
```

---

### LLMOps on Azure

| Component | Azure Service | What It Does |
|---|---|---|
| **Prompt versioning** | Azure AI Foundry Prompt Flow | Version prompts like code, A/B test prompts |
| **LLM evaluation** | Azure AI Evaluation SDK | Score faithfulness, groundedness, safety |
| **Model registry** | Azure AI Foundry Model Catalog | Track which model version is in production |
| **Experiment tracking** | Azure AI Foundry + MLflow | Track prompt changes, model versions, eval scores |
| **Tracing** | Application Insights + Langfuse | Trace every LLM call with tokens, cost, latency |
| **Content safety** | Azure Content Safety | Safety guardrails on input/output |
| **CI/CD for LLMs** | GitHub Actions + DeepEval | Block deployment if eval score drops |
| **Cost monitoring** | Azure Cost Management + Custom Metrics | Alert on LLM spend spikes |
| **Fine-tuning** | Azure AI Foundry fine-tune | Customize GPT-4o on domain data |

**Azure Prompt Flow (LLMOps pipeline):**
```yaml
# flow.dag.yaml — defines your RAG pipeline as versionable YAML
inputs:
  question:
    type: string

nodes:
  - name: embed_query
    type: python
    source: embed.py
    inputs:
      query: ${inputs.question}

  - name: vector_search
    type: python
    source: search.py
    inputs:
      embedding: ${embed_query.output}

  - name: generate
    type: llm
    source: generate.jinja2
    connection: azure_openai_conn
    inputs:
      context: ${vector_search.output}
      question: ${inputs.question}

outputs:
  answer:
    type: string
    reference: ${generate.output}
```

---

### LLMOps on AWS

| Component | AWS Service | What It Does |
|---|---|---|
| **Prompt versioning** | Bedrock Prompt Management | Version and test prompts, A/B testing |
| **LLM evaluation** | Bedrock Model Evaluation | Automated quality and safety scoring |
| **Model registry** | SageMaker Model Registry | Track LLM version deployed to each endpoint |
| **Experiment tracking** | SageMaker Experiments + MLflow | Track fine-tuning runs, eval scores |
| **Tracing** | CloudWatch + X-Ray + Langfuse | Full observability on every Bedrock call |
| **Content safety** | Bedrock Guardrails | PII, topic, grounding, safety on all calls |
| **CI/CD for LLMs** | CodePipeline + Lambda eval | Automated eval before promoting new model |
| **Cost monitoring** | Cost Explorer + CloudWatch | Token usage and cost per model/app |
| **Fine-tuning** | Bedrock fine-tuning / SageMaker | Fine-tune Titan, Llama on your data |

---

## Part 7 — DevOps

### What is DevOps for AI?

DevOps for AI extends standard software DevOps (plan → code → build → test → deploy → monitor) with AI-specific stages (data versioning, model validation, eval gating, LLM quality tests).

```
Plan → Code → Build → [Eval Gate] → Test → Deploy → Monitor → Feedback
```

---

### DevOps Pipeline for RAG Chatbot on Azure

```yaml
# GitHub Actions — .github/workflows/deploy.yml

name: RAG Chatbot CI/CD

on:
  push:
    branches: [main]

env:
  ACR_NAME: myregistry.azurecr.io
  APP_NAME: rag-chatbot-api
  RESOURCE_GROUP: prod-rg

jobs:

  # ── STAGE 1: Unit Tests ─────────────────────────────────────────
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest tests/unit/ -v

  # ── STAGE 2: LLM Quality Gate ────────────────────────────────────
  llm-eval:
    needs: unit-test
    runs-on: ubuntu-latest
    steps:
      - name: Run DeepEval LLM tests
        env:
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_API_KEY }}
        run: |
          pip install deepeval
          deepeval test run tests/llm/  # Fails if faithfulness < 0.8

  # ── STAGE 3: Build Docker Image ──────────────────────────────────
  build:
    needs: llm-eval
    runs-on: ubuntu-latest
    steps:
      - name: Login to ACR
        run: az acr login --name ${{ secrets.ACR_NAME }}
      - name: Build and push image
        run: |
          docker build -t $ACR_NAME/$APP_NAME:${{ github.sha }} .
          docker push $ACR_NAME/$APP_NAME:${{ github.sha }}

  # ── STAGE 4: Deploy to Staging ───────────────────────────────────
  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging Container Apps
        run: |
          az containerapp update \
            --name $APP_NAME-staging \
            --resource-group staging-rg \
            --image $ACR_NAME/$APP_NAME:${{ github.sha }}
      - name: Run smoke tests
        run: pytest tests/smoke/ --base-url https://staging.api.example.com

  # ── STAGE 5: Deploy to Production ────────────────────────────────
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production     # Requires manual approval in GitHub
    steps:
      - name: Blue/green deploy to production
        run: |
          az containerapp update \
            --name $APP_NAME \
            --resource-group $RESOURCE_GROUP \
            --image $ACR_NAME/$APP_NAME:${{ github.sha }} \
            --revision-suffix ${{ github.sha }}
```

---

### DevOps Pipeline for RAG Chatbot on AWS

```yaml
# buildspec.yml — for AWS CodeBuild

version: 0.2
phases:
  install:
    commands:
      - pip install -r requirements.txt
      - pip install deepeval pytest

  pre_build:
    commands:
      - echo "Running LLM quality gate..."
      - deepeval test run tests/llm/     # Block pipeline if quality drops
      - echo "Logging in to ECR..."
      - aws ecr get-login-password | docker login --username AWS
          --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

  build:
    commands:
      - docker build -t rag-chatbot:$CODEBUILD_RESOLVED_SOURCE_VERSION .
      - docker tag rag-chatbot:$CODEBUILD_RESOLVED_SOURCE_VERSION
          $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/rag-chatbot:$CODEBUILD_RESOLVED_SOURCE_VERSION

  post_build:
    commands:
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/rag-chatbot:$CODEBUILD_RESOLVED_SOURCE_VERSION
      - printf '[{"name":"rag-chatbot","imageUri":"%s"}]'
          $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/rag-chatbot:$CODEBUILD_RESOLVED_SOURCE_VERSION
          > imagedefinitions.json

artifacts:
  files: imagedefinitions.json
```

---

### IaC (Infrastructure as Code)

**Azure — Bicep:**
```bicep
// main.bicep — provision Container Apps + Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-rag-prod'
  location: resourceGroup().location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'rag-chatbot-api'
  location: resourceGroup().location
  properties: {
    template: {
      containers: [{
        name: 'api'
        image: 'myregistry.azurecr.io/rag-chatbot:latest'
        resources: { cpu: '0.5', memory: '1Gi' }
      }]
      scale: { minReplicas: 1, maxReplicas: 20 }
    }
  }
}
```

**AWS — CDK (Python):**
```python
from aws_cdk import Stack, aws_ecs as ecs, aws_ecs_patterns as ecs_patterns

class RagChatbotStack(Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        # ECS Fargate service with ALB
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "RagChatbotService",
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(ecr_repo, tag="latest"),
                container_port=8000,
            ),
            cpu=512,
            memory_limit_mib=1024,
            desired_count=2,
        )

        # Auto-scaling
        scaling = fargate_service.service.auto_scale_task_count(max_capacity=20)
        scaling.scale_on_cpu_utilization("CpuScaling", target_utilization_percent=70)
```

---

## Part 8 — End-to-End DevOps + MLOps + LLMOps Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DEVELOPER WORKFLOW                           │
│                                                                     │
│  1. Engineer writes RAG code + prompt + tests                       │
│  2. Push to GitHub → triggers CI/CD pipeline                        │
│                                                                     │
│  ┌──── CI Pipeline ────────────────────────────────────────────┐   │
│  │  Unit tests → LLM eval (DeepEval) → Build Docker → Push ACR │   │
│  │  ↓ FAILS if: unit test fails OR faithfulness < 0.8           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──── CD Pipeline ────────────────────────────────────────────┐   │
│  │  Deploy staging → Smoke test → Manual approval → Prod deploy │   │
│  │  Blue/green: new version gets 10% traffic → 100% if healthy  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      PRODUCTION MONITORING                          │
│                                                                     │
│  Infrastructure:  Azure Monitor / CloudWatch                        │
│  APM:             App Insights / X-Ray                              │
│  LLM Traces:      Langfuse (every call: tokens, cost, latency)      │
│  LLM Quality:     RAGAS (sample 5% of requests for eval score)      │
│  Security:        Content Safety + Guardrails (every request)       │
│  Cost:            Budget alerts at 80% and 100% threshold           │
│                                                                     │
│  Alert conditions:                                                  │
│  → Error rate > 1%        → PagerDuty → On-call engineer            │
│  → p95 latency > 5s       → Slack notification                      │
│  → Faithfulness < 0.75    → Trigger prompt review workflow          │
│  → Cost spike > 2×        → Slack + automatic scaling cap           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                        MLOPS / LLMOPS LOOP                          │
│                                                                     │
│  1. Data drifts (new documents, new question types)                 │
│  2. RAGAS quality drops below threshold                             │
│  3. Auto-trigger: re-index new documents, re-evaluate chunking      │
│  4. Prompt engineer updates prompt → PR → eval gate → deploy        │
│  5. If model version changes (gpt-5.4 → gpt-5.5):                  │
│     → Run full eval suite on both versions                          │
│     → A/B test in staging                                           │
│     → Promote if quality ≥ current version                          │
│  6. Fine-tune model on domain data if base model quality plateaus   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Part 9 — Quick Decision Cheat Sheet

### Which service for what?

| Need | Azure | AWS |
|---|---|---|
| Deploy a FastAPI chatbot | Container Apps | ECS Fargate / App Runner |
| Store PDFs for RAG | Blob Storage | S3 |
| Vector search | Azure AI Search | OpenSearch |
| LLM (OpenAI models) | Azure OpenAI | ❌ (use Azure or direct API) |
| LLM (Claude) | ❌ (use Bedrock) | Bedrock |
| Cheapest LLM | Nova Micro on Bedrock | Nova Micro on Bedrock |
| Managed RAG pipeline | AI Search + Prompt Flow | Bedrock Knowledge Bases |
| Managed agents | AI Foundry Agents | Bedrock Agents |
| Content safety | Azure Content Safety | Bedrock Guardrails |
| PDF extraction | Document Intelligence | Textract |
| Chat history | Cosmos DB | DynamoDB |
| Session cache | Redis Cache | ElastiCache |
| Async job queue | Service Bus | SQS |
| CI/CD | Azure DevOps / GitHub Actions | CodePipeline / GitHub Actions |
| Model training | Azure ML | SageMaker |
| Secret storage | Key Vault | Secrets Manager |
| Enterprise auth | Entra ID | Cognito |
| Monitor everything | Azure Monitor + App Insights | CloudWatch + X-Ray |
| IaC | Bicep / Terraform | CDK / CloudFormation / Terraform |
| Container registry | ACR | ECR |
