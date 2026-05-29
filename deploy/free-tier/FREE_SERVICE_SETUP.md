# Free-Service Setup

Use this for a prototype or demo without paying for infrastructure.

## 1. Database

Create a free Neon Postgres project and copy the pooled connection string.

Set both:

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST/neondb?ssl=require
SYNC_DATABASE_URL=postgresql://USER:PASSWORD@HOST/neondb?ssl=require
```

## 2. Queue/cache

Create a free Upstash Redis database and copy the Redis URL.

```env
REDIS_URL=rediss://default:PASSWORD@HOST:PORT
```

## 3. Backend

Deploy `backend/` as a Docker web service.

Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Deploy a second service from the same image for the worker:

```bash
dramatiq app.workers.tasks
```

## 4. Frontend

Deploy `frontend/` to Vercel, Netlify, or Cloudflare Pages.

```env
NEXT_PUBLIC_API_BASE_URL=https://your-api-host.example
```

## 5. Zero-paid demo mode

Keep these enabled until API keys are ready:

```env
AI_FREE_DEMO_MODE=true
SCRAPER_FREE_DEMO_MODE=true
TRANSCRIPT_FREE_DEMO_MODE=true
```

## 6. Live mode

Disable demo mode and add keys:

```env
AI_FREE_DEMO_MODE=false
SCRAPER_FREE_DEMO_MODE=false
TRANSCRIPT_FREE_DEMO_MODE=false
GROK_API_KEY=
GEMINI_API_KEY=
APIFY_API_TOKEN=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Free tiers can change and can suspend, expire, or throttle services. For real production, budget for paid Postgres, Redis, scraping, AI, and worker capacity.
