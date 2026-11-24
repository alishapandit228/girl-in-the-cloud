# Delivery and acceptance

Girl in the Cloud is Alisha Pandit’s full-stack portfolio. Visitors can explore project islands, read case studies, inspect a learning architecture and contact the owner. The admin area reports real traffic and accepted contact submissions. Deployment to a public web host remains an owner configuration step.

## Approved design decisions

| # | Decision | Implementation and acceptance boundary |
|---|---|---|
| 1 | Hybrid portfolio | Scrolling home, project pages, article pages, certificates, résumé and owner routes |
| 2 | Soft Girl Meets Tech hero | Editorial introduction, project/résumé links, cloud artwork, floating technical marks, labelled portrait slot and conditional LinkedIn |
| 3 | Floating navigation dock | Seven named destinations, active section, magnification, focus and mobile layout |
| 4 | Cloud Wonderland | Day/night sky, soft lighting, particles, parallax and illustrated fallback. Desktop 3D viewer has connected servers, animated packet and orbit controls |
| 5 | Project islands | Four distinct original isometric illustrations open project case studies with scope, challenges, architecture, status and optional external assets |
| 6 | Skills architecture | Five connected layers with keyboard/touch technology controls and experience/learning descriptions |
| 7 | Journey and diary | Education and leadership context, certification timeline, paper gallery and optional captioned photographs |
| 8 | Workspace and editorial about | Six desk objects with equivalent named buttons, WebGL scene and lightweight fallback |
| 9 | Telephone booth | Illustrated booth alongside form, GitHub, résumé and configurable social/email links |
| 10 | Day and night themes | Local-time switching, manual mode, persistence and coordinated illustration lighting |
| 11 | Boot and reveal | Short, skippable, nonblocking entrance with logo and three messages; session-level replay control and reduced-motion handling |
| 12 | Cloud cursor | Supplemental cloud on fine desktop pointers; touch and reduced-motion exclusions |
| 13 | Typography | Cormorant Garamond and Inter bundled by Vite with system fallbacks |
| 14 | AP emblem | Transparent ribbon seal, separate night variant and favicon |
| 15 | Professional résumé | PDF view/download integration and explicitly labelled missing-asset page. Real document and ATS review pending |
| 16 | Additional features | Detailed below |

## Functional requirements

| # | Feature | Evidence and remaining dependency |
|---|---|---|
| 1 | GitHub | Public REST profile, repositories, stars, languages and activity. GraphQL calendar, 10-minute caching, timeout, partial errors and stale fallback. Production token required for calendar |
| 2 | Demos and source | AI Resume Analyser public source verified. Private projects and unverified live URLs omit external buttons |
| 3 | Certificate viewer | Issue date/issuer metadata, image and PDF branches, download and issuer links. Public certificate assets and issuer URLs pending |
| 4 | Currently learning | Configurable status, goal, resources and completed milestones |
| 5 | Blog | Markdown listing, search, category, tags, reading time, headings, syntax highlighting, sharing, related articles and metadata. Draft stays unpublished |
| 6 | Analytics | Expiring owner session, logout, date filters, traffic charts, visitor-day estimates, project pages, devices, domain referrers, downloads and contact receipts |
| 7 | Contact email | Validation, honeypot, rate limits, delivery feedback, SMTP TLS and a local Mailpit profile. Live sender and recipient configuration pending |
| 8 | Health and performance | Database-backed health endpoint, optional release metadata, public CI link, private response timing and process age |
| 9 | SEO | Server-rendered page metadata, canonical URLs, share card, structured data, sitemap, robots, custom 404 and private noindex pages |
| 10 | Accessibility | Native semantic routes, visible focus, named keyboard controls, reduced motion, WebGL fallback, narrow-screen layout and automated homepage audit. Manual assistive-technology certification remains outside the measured results |

## Release materials

[Architecture](ARCHITECTURE.md) · [Design](DESIGN_GUIDELINES.md) · [Deployment, commands and recovery](DEPLOYMENT.md) · [Security](SECURITY.md) · [Test results](TEST_REPORT.md) · [Personal assets and credentials](ASSET_REQUIREMENTS.md)

The server-rendered interface uses Jinja and native CSS/navigation. React and Three.js handle the optional 3D scenes. This keeps public content usable during JavaScript or GPU failures. GitHub Actions is the verification environment for npm, Docker, PostgreSQL, real local SMTP, browser screenshots and Lighthouse.
