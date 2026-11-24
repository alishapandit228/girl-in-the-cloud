Initial repository README and runtime inspected. Local Chromium and FastAPI available. Docker CLI unavailable.
Content parsed with Python JSON. Original SVGs parsed with ElementTree. Browser interaction checks follow after route integration.
FastAPI TestClient returned 200 for home, LabQuest, blog, first certificate, admin sign-in, service status, résumé, health and sitemap. Unknown route returned 404.
Seven unittest groups passed locally (routes, metadata, owner privacy, CSRF, login throttling, contact validation and SMTP mocks, Markdown publishing, GitHub cache/failure). Browser startup was denied by the local runtime (Chromium process singleton socket). Docker and npm registry access are unavailable here. GitHub Actions is configured to build, test Compose and run Chromium/Lighthouse on a hosted runner.

## Hosted production stack

Run 45437415566 on commit 3270834 passed Pytest, Vitest, TypeScript/Vite production build, Compose startup with PostgreSQL/Alembic and Nginx, Playwright on desktop and mobile, Lighthouse and dependency audits. The Chromium screenshots showed the desktop plate mid-reveal after reload. Changed the reveal to run only during the first entrance and to finish on Skip.

Lighthouse mobile homepage scores: performance 98, accessibility 100, best practices 100, SEO 100. FCP 1.83 s, LCP 1.86 s, total blocking time 0 ms. These are hosted CI lab measurements on localhost. The warm in-process development homepage measured 2.42 ms median across 20 requests, excluding network and browser rendering.
Nine backend test groups now include fixture-based résumé download and certificate media tests, GitHub REST and GraphQL contract tests, private analytics and SMTP failure cases. The hosted workflow also exercises a real SMTP submission against an isolated Mailpit inbox.
Adding Mailpit exposed a Compose address collision on the edge network in run 45438383708. Reserved a separate dynamic IP pool so other services cannot take the fixed trusted-proxy address.
Run 45438884550 passed the expanded container startup and Playwright form-to-Mailpit check. Reviewed day, night and mobile browser screenshots. Lighthouse reported 99 performance, 100 accessibility, 100 best practices and 100 SEO. The successful npm resolution is committed as frontend/package-lock.json; build and CI now use npm ci.
Locked-build run 45439958183 passed production startup, SMTP receipt, owner login, date filtering and logout. Its individual mobile Lighthouse run scored 74/100/100/100 (performance/accessibility/best practices/SEO; FCP 2.1 s, LCP 2.6 s, TBT 920 ms, CLS 0). Earlier runs scored 98 and 99 for performance. Reduced mobile compositing, deferred below-fold paint and added three cold-navigation samples per verification run.
