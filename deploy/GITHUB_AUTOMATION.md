# GitHub Automation

This project includes GitHub Actions for testing, demo automation, and optional deployment.

## Workflows

- `CI`: runs backend tests, frontend build, and Docker build checks on pushes and pull requests.
- `Demo Automation`: runs the free local automation demo manually or every day at 09:17 UTC.
- `Deploy`: optionally triggers Render and Vercel deployments from `main`.

## Required repository setup

Create a GitHub repository, upload this project, then enable Actions.

For free demo mode, no secrets are required to run `Demo Automation`.

For deployment, add these repository secrets as needed:

```text
RENDER_DEPLOY_HOOK_URL
VERCEL_TOKEN
VERCEL_ORG_ID
VERCEL_PROJECT_ID
```

For live AI/scraping workflows, add these as environment variables on your backend host, not in plain text:

```text
GROK_API_KEY
GEMINI_API_KEY
APIFY_API_TOKEN
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
```

## Upload path

1. Create a new empty repo on GitHub.
2. Upload the contents of this project.
3. Open the `Actions` tab.
4. Run `Demo Automation` manually.
5. Confirm the workflow prints the demo job, comments, transcript, fact-check JSON, and publish payload.

The GitHub plugin currently has no accessible repositories for this account. Once a repo exists and the GitHub app is installed on it, Codex can push files there directly.
