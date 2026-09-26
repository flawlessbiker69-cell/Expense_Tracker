# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Spendly: a Flask + SQLite expense tracker with server-rendered Jinja2 templates, plain CSS/JS, and no ORM or frontend framework. It is a step-based tutorial scaffold: `app.py` marks unimplemented features with "coming in Step N" placeholder routes (logout, profile, expense add/edit/delete), and `database/db.py` is a comment-only stub describing the intended `get_db()` / `init_db()` / `seed_db()` (SQLite connection with `row_factory` and foreign keys enabled, `CREATE TABLE IF NOT EXISTS`, sample data). Login and register pages only render forms; there is no auth or persistence yet.

## Commands

The virtualenv lives one level above the repo root (`../venv`, outside git), and shell activation does not persist between commands, so call its interpreter directly from the repo root:

```
../venv/bin/pip install -r requirements.txt
../venv/bin/python app.py          # dev server, debug mode, http://127.0.0.1:5001
../venv/bin/python -m pytest       # pytest + pytest-flask are installed; no tests exist yet
../venv/bin/python -m pytest path/to/test_file.py::test_name   # single test
```

There is no linter or build step configured. The dev server runs on port 5001, not Flask's default 5000.

## Architecture

- `app.py` holds all routes and calls `render_template`. Every page extends `templates/base.html`, which provides the navbar, footer (including the Terms and Privacy links) and the `title`, `head`, `content` and `scripts` blocks. Link between pages with `url_for(...)`.
- Styling is split across two files, and both are loaded on the landing page:
  - `static/css/style.css` holds the design tokens (CSS variables such as `--accent` and `--font-display`), a global reset that zeroes all margins and padding, and shared component styles.
  - `static/css/landing.css` is loaded only by `landing.html` (via its `head` block) and holds the hero and video-modal styles, all using the `lp-*` class prefix. The old `.hero` and `.mock-*` rules in `style.css` are now unused.
- `terms.html` and `privacy.html` reuse the auth page classes (`auth-section`, `auth-container`, `auth-card`) plus `legal-*` modifiers defined in `style.css`.
- The landing page video modal is vanilla JS inline in `landing.html`'s `scripts` block. It sets the iframe `src` on open and clears it on close so the video stops. The YouTube URL is a placeholder in the `data-video-src` attribute of `#video-modal`.
- `static/js/main.js` is effectively empty.

## Gotchas

- The `.git` repo root is the inner `expense-tracker/` folder; the outer folder holds `venv/`, `__MACOSX/` and other non-repo files, so run git commands from the inner one.
- `.gitignore` already excludes `spendly.db`, so the SQLite file is expected to be created at the repo root once `db.py` is implemented.
- The "See how it works" hero button and the `support@spendly.example` address on the privacy page are placeholders.
