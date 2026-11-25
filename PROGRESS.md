# Release status

**Application revision:** 2edbf52ac663f4aef994cf5c323ae49479f6419f on main. Hosted verification passed, including three mobile Lighthouse measurements.

The public portfolio, optional WebGL scenes, publishing system, FastAPI services, private dashboard and Docker deployment stack are implemented. GitHub Actions built the locked frontend, migrated PostgreSQL, started Nginx and Mailpit, and exercised public and private browser flows. The repository includes real browser previews for desktop, mobile and night mode.

| Release step | Status |
|---|---|
| Source and infrastructure | Pushed to main, committed tree checked against GitHub |
| Local development | Python/SQLite startup or Compose, generated local environment, documented in README and DEPLOYMENT |
| Personal assets | Owner-approved portrait, résumé, certificate scans/verification URLs, event photos, LinkedIn, project demos and screenshots remain configurable |
| Blog | Editorial draft excluded from public routes until approved for publication |
| Live delivery | SMTP inbox tested with Mailpit. Production mailbox and credentials required |
| Public deployment | No public host configured. Requires an existing HTTPS host, production environment and release smoke check |

**Next release action:** configure the approved assets and production environment described in ASSET_REQUIREMENTS.md and DEPLOYMENT.md, then deploy the tested revision to the selected host. The latest remote SHA is also available in the repository commit history.

[Acceptance matrix](DELIVERY.md) · [Verification report](TEST_REPORT.md) · [Hosted verification](https://github.com/alishapandit228/girl-in-the-cloud/actions/runs/45440661689)

Render Free deployment blueprint prepared for a user-owned Neon Free database. Public launch requires connecting those accounts and entering DATABASE_URL and ADMIN_HASH. Personal publication assets await owner selection.
