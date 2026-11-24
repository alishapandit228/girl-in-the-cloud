Initial repository README and runtime inspected. Local Chromium and FastAPI available. Docker CLI unavailable.
Content parsed with Python JSON. Original SVGs parsed with ElementTree. Browser interaction checks follow after route integration.
FastAPI TestClient returned 200 for home, LabQuest, blog, first certificate, admin sign-in, service status, résumé, health and sitemap. Unknown route returned 404.
Seven unittest groups passed locally (routes, metadata, owner privacy, CSRF, login throttling, contact validation and SMTP mocks, Markdown publishing, GitHub cache/failure). Browser startup was denied by the local runtime (Chromium process singleton socket). Docker and npm registry access are unavailable here. GitHub Actions is configured to build, test Compose and run Chromium/Lighthouse on a hosted runner.

## Hosted production stack

Run 45437415566 on commit 3270834 passed Pytest, Vitest, TypeScript/Vite production build, Compose startup with PostgreSQL/Alembic and Nginx, Playwright on desktop and mobile, Lighthouse and dependency audits. The Chromium screenshots showed the desktop plate mid-reveal after reload. Changed the reveal to run only during the first entrance and to finish on Skip.

Lighthouse mobile homepage scores: performance 98, accessibility 100, best practices 100, SEO 100. FCP 1.83 s, LCP 1.86 s, total blocking time 0 ms. These are hosted CI lab measurements on localhost. The warm in-process development homepage measured 2.42 ms median across 20 requests, excluding network and browser rendering.
