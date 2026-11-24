# Personal assets and publishing

Only place material approved for publication in this public repository. All paths in personal content are relative site URLs. Restart/redeploy after editing JSON.

| Item | Where to add it | Current behavior |
|---|---|---|
| Portrait | Place an optimized portrait in frontend/public/media and set portrait to /assets/media/portrait.webp | Labelled AP placeholder |
| Résumé | Add an approved, text-selectable, single-column PDF to frontend/public/media/resume.pdf and set resume to /assets/media/resume.pdf | Résumé page explains availability |
| Certificates | Set each certificates entry’s file and verify fields to an approved PDF/image path and issuer verification URL | Date and issuer shown |
| Project media | Add screenshots as objects with src and alt in the project’s screenshots array | Original illustrations shown |
| Demo and documentation | Set project demo, docs, source and deployment fields after verifying public access | Only configured URLs appear |
| Social contacts | Set linkedin and email to the approved professional profile and mailbox | Missing links omitted |
| Event photographs | Add approved, captioned photos to the gallery array with src, alt and caption | Achievement cards remain text-based until supplied |
| Learning | Edit learning names, statuses, goals, milestones and resource mapping | Current learning goals appear as expandable items |
| Personal story | Edit intro, title, academic details, workspace object text and skills | Public render uses the JSON on process start |

LabQuest and DeployHub repositories were private during setup. The AI Resume Analyser public README documents the matching implementation. No live project URL or shareable certificate scan was supplied. Keep public copy accurate when projects change status.

## Publish a field note

Create a .md file in content/blogs. The first line is a JSON object. Write Markdown underneath it. Each published entry needs a unique URL-safe slug and an ISO publication date. Example metadata:

```json
{"title":"Article title","slug":"article-title","category":"Linux","tags":["Shell"],"status":"draft","date":null,"summary":"Short description"}
```

The Linux article supplied with the project is an editorial draft. After reviewing content and attribution, set status to published and supply a date. The listing, navigation, search, reading time, related links, table of contents and sitemap derive from the published files.
