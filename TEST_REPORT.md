# Verification report

**Application under test:** 2edbf52ac663f4aef994cf5c323ae49479f6419f. The final report commit changes documentation only.

## Checks

| Check | Method and scope |
|---|---|
| Backend | Nine Pytest groups for public routes, custom 404, metadata and privacy, authentication, CSRF, login limiting, contact handling, publishing, asset fixtures and GitHub contracts/cache |
| Frontend | Locked npm install, Vitest and React Testing Library fallback test, TypeScript type check and Vite production build |
| Live GitHub | Profile, repository statistics, languages, recent activity and GraphQL contribution calendar available during hosted integration test |
| Containers | Docker Compose built the multi-stage application, started PostgreSQL, applied Alembic migration, waited for Nginx and confirmed /api/health |
| Browser | Chromium desktop and mobile navigation, theme persistence, boot skip/replay, workspace, skills, project routing, blog search, narrow viewport and reduced-motion fallback |
| Admin | Real browser login against PostgreSQL, date-filtered traffic report, accepted contact count and logout. API tests cover unauthorized reads and cross-origin writes |
| Email | Browser form submission accepted by SMTP and present in Mailpit; unit tests cover missing configuration and service failure |
| Accessibility | Automated Lighthouse homepage audit, keyboard-focused object selection, named controls, reduced motion and responsive layout. Manual assistive-technology testing was not performed |
| Secrets | Searched tracked filenames and content for environment files, private keys and common token formats. Git ignores local database, credentials and generated dependencies |
| Dependencies | pip-audit of backend requirements and npm audit of production packages |
| Assets | SVGs parsed, JSON validated, résumé fixture downloaded, certificate PDF/image branches rendered, desktop/mobile/night screenshots inspected |

Run locally with `python -m unittest discover -s tests -p test_app.py`, then `npm ci && npm test && npm run build` in frontend. For the complete multi-service suite, the authoritative commands live in .github/workflows/verify.yml.

## Fixes found by testing

- A desktop screenshot captured the hero reveal after a reload. The entrance now runs in the first-visit window only and ends when skipped.
- Enabling Mailpit exposed an address collision with Nginx. A dedicated dynamic subnet range now excludes the trusted fixed proxy address.
- Single hosted Lighthouse performance measurements ranged from 74 to 99. The mobile layout now defers below-fold sections, removes expensive mobile compositing and throttles scroll work. CI collects three independent navigation measurements per run.

## Measurement limits

Hosted Chromium tests run against the production Compose stack on localhost. Lighthouse uses a simulated mobile network and CPU. Real-user latency, search indexing, SMTP delivery to a production inbox, uptime, the chosen hosting environment and assistive-technology compatibility require verification after deployment. The CI token is ephemeral; production needs its own GitHub credential for the calendar.

## Final results

All verification steps passed in [GitHub Actions run 45440661689](https://github.com/alishapandit228/girl-in-the-cloud/actions/runs/45440661689). Nine backend tests and the React fallback test passed. The dependency audit gates passed.

| Mobile Lighthouse metric | Run 1 | Run 2 | Run 3 | Median |
|---|---:|---:|---:|---:|
| performance | 98 | 98 | 98 | 98 |
| accessibility | 100 | 100 | 100 | 100 |
| best-practices | 100 | 100 | 100 | 100 |
| seo | 100 | 100 | 100 | 100 |
| first-contentful-paint (ms) | 1825 | 1830 | 1833 | 1830 |
| largest-contentful-paint (ms) | 1900 | 1905 | 1908 | 1905 |
| total-blocking-time (ms) | 0 | 0 | 0 | 0 |

Render launch configuration: parsed the blueprint, verified the single Free instance, checked shell syntax, and exercised startup with stand-in migration/server commands. Verified PostgreSQL driver selection, TLS parameter preservation, platform URL, port, version and rejection of invalid database URLs. Nine backend test groups passed locally. A live Render service and production mailbox have not been verified.
