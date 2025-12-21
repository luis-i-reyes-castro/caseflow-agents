# wa-agents

A Python API for my WhatsApp chatbot apps

## Installation

### As an Editable Package

```bash
git clone https://github.com/luis-i-reyes-castro/wa-agents.git
pip install -e wa-agents/
```

### As a Dependency

Add this line to your `requirements.txt`:
```bash
wa-agents @ git+https://github.com/luis-i-reyes-castro/wa-agents.git@main
```

Re-run `pip`:
```bash
pip install -r requirements.txt
```

## Required Environment Variables

### Digital Ocean Spaces S3 Bucket

|                     |     |
| ------------------- | --- |
| `BUCKET_NAME`       | Bucket Name                  |
| `BUCKET_REGION`     | Bucket Region (e.g., `atl1`) |
| `BUCKET_KEY`        | Bucket Access Key ID         |
| `BUCKET_KEY_SECRET` | Bucket Secret Access Key     |

### LLM API

At least one of the following:
* `OPENROUTER_API_KEY`
* `OPENAI_API_KEY`
* `MISTRAL_API_KEY`

### Queue Database

* `QUEUE_DB_NAME` (Optional. Default value is `queue.sqlite3`.)

### WhatsApp

* `WA_TOKEN`
* `WA_VERIFY_TOKEN`
