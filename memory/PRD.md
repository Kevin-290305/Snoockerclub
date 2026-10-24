# Snooker Club Salto – Vercel fix
Problem: user saw `npm warn Unknown env config "cache-dir"` in Vercel deploy logs.
- Diagnosis (Jun 2026): warning is harmless (Vercel build env); deploys are "Ready". Production https://snoockerclub.vercel.app renders all sections (hero, clube, galeria, campeonatos, lives, horários, contato).
- Fix: js/site.js reveal-on-scroll made robust (threshold 0 + 2.5s fallback) so sections never stay invisible when jumping via menu. Fixed copy at /app/snookerclub-fix.
- Not done: push to GitHub repo Kevin-290305/Snookerclub (private, no access from this workspace).
Backlog: P1 host /api backend (campeonatos/inscrições/admin) – currently 404 on Vercel; P2 deploy from single main branch instead of conflict_220926_1926.
