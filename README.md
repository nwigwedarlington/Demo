# Facebook Video Fact-Check Automation Platform

Production-oriented starter for the pasted automation spec, built without n8n.

## Free-service deployment path

This repo runs fully on local Docker for free. For a small hosted demo, use:

- Backend/container host: Render, Koyeb, Fly.io, or another free/low-cost container host.
- Frontend: Vercel, Netlify, or Cloudflare Pages.
- Postgres: Neon free plan.
- Redis: Upstash Redis free plan.
- AI/scraping: provider keys are required. Gemini has free-tier options; xAI Grok and Apify may require paid credits depending on usage.

Current public free-tier checks used while preparing this scaffold:

- Upstash Redis pricing lists a Free plan with 256 MB and 500K monthly commands: https://upstash.com/pricing/redis
- Neon describes a Free Postgres plan with 0.5 GB storage per project and usage caps: https://neon.com/faqs/postgres-services-free-to-production

Treat free tiers as demo/prototype infrastructure, not guaranteed production capacity.

## Stack

- Python 3.12, FastAPI, AsyncIO, SQLAlchemy, Pydantic
- PostgreSQL, Redis, Dramatiq
- httpx, Playwright-compatible scraper fallback hooks
- Next.js, TypeScript, TailwindCSS
- Docker Compose plus Kubernetes-ready manifests

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Open:

- API: http://localhost:8000/docs
- Dashboard: http://localhost:3000

Submit a job:

```bash
curl -X POST http://localhost:8000/jobs \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://www.facebook.com/example/videos/123\",\"source_type\":\"video\"}"
```

## Free/local modes

Set these for a zero-paid local demo:

```env
AI_FREE_DEMO_MODE=true
SCRAPER_FREE_DEMO_MODE=true
TRANSCRIPT_FREE_DEMO_MODE=true
```

In demo mode the app uses deterministic mock data while preserving the real workflow, database schema, queueing, failure handling, and dashboard.

## Important legal/platform note

Facebook data collection must follow Facebook/Meta terms, local law, and privacy rules. Prefer official APIs or licensed services. The Playwright fallback is intentionally isolated behind configuration and should be used only where allowed.
