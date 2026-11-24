# Architecture

The browser requests HTML through Nginx. FastAPI renders Jinja templates from version-controlled JSON and Markdown. Static CSS and JavaScript enhance the public pages. Vite compiles React, TypeScript, Three.js, React Three Fiber and Drei into a separate desktop workspace bundle. Its initializer waits for the workspace to enter the viewport. Keyboard buttons and an original lightweight illustration remain available on every device.

Public pages use server routing and server-rendered metadata. This makes case studies and published articles readable by crawlers and before JavaScript loads. Native navigation, CSS transitions, SVG icons and HTML meters implement the router, motion, icon and dashboard chart requirements without extra client dependencies. There is no separate SPA deployment.

## Persistence

FastAPI uses parameterized SQL through SQLAlchemy on PostgreSQL. Alembic migrates the production database. A standard-library SQLite adapter provides local persistence with the same schema and allows local testing without a database service.

| Table | Purpose |
|---|---|
| sessions | HMAC of opaque owner token and expiry |
| limits | Expiring, keyed counters for login and contact requests |
| events | UTC day, daily visitor estimate, route, event, device and referrer domain |
| contacts | Timestamp, random receipt identifier and SMTP acceptance status |

GitHub REST requests fetch public account, repository and event data. GraphQL provides the annual contribution calendar when a token is configured. A process-local lock coalesces concurrent refreshes. Cached snapshots expire after ten minutes. When refresh fails an older snapshot can be returned with a notice. SMTP submission happens server-side. Inbox content stays at the configured mail provider.

## API

| Method and path | Access and behavior |
|---|---|
| GET /api/health | Public database connectivity and release version |
| GET /api/github | Public cached GitHub data with partial availability |
| POST /api/contact | Validated, throttled email submission |
| POST /api/login | Throttled single-owner authentication |
| POST /api/logout | Invalidates the current owner session |
| GET /api/report?start=YYYY-MM-DD&end=YYYY-MM-DD | Authenticated aggregates and accepted contact receipts |

Private runtime metrics include a rolling sample of request processing time and process age. Public status draws release metadata from the hosting environment. Neither source measures historical uptime.
