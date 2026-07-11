# Enterprise frontend redesign

## Goal

Rebuild Minitower's frontend to look like enterprise SaaS software (Salesforce/ServiceNow/Jira-class) instead of a stock Bootstrap prototype, using a light corporate-gray palette with a single blue accent. Visual layer only — no new pages, no URL/view/model changes.

## Scope

- All 11 existing templates get restyled: `home/index.html`, `home/about.html`, `inventory/inventory_base.html`, `inventory/host_profile.html`, `hosts/add_hosts.html`, `firewall/firewall_base.html`, `firewall/fwrule.html`, `firewall/add_firewall.html`, `firewall/add_firewallmodal.html`, `upload/host-data-upload.html`, `upload/fw-data-upload.html`.
- Navigation restructured from a top navbar with dropdowns to a persistent left sidebar + slim top bar.
- Framework migration: Bootstrap 4.5.3 + jQuery → Bootstrap 5 + vanilla JS, including the `django-bootstrap-modal-forms` JS integration.
- Out of scope: new features, URL changes, model/view changes, mobile-specific layout work (internal desktop ops tool).

## Design decisions (from brainstorming)

| Decision | Choice |
|---|---|
| Layout | Sidebar (nav) + top bar (page title + context-aware search) |
| Theme | Light corporate gray — sidebar `#2d3340`, top bar `#ffffff` (border `#e2e5ea`), content bg `#f4f5f7`, cards/tables `#ffffff`, body text `#1f2328` |
| Accent | Corporate blue `#2f5aad`, hover `#24478a` — used for links, primary buttons, active sidebar item, table header accents |
| Status badges | Muted pills — up: bg `#e6f4ea` / text `#1e7e34`; down: bg `#fbe9e9` / text `#b42318` |
| Frontend stack | Bootstrap 5 (vendored, no CDN) + vanilla JS, dropping jQuery entirely |
| Typography | System font stack (`-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`) — no webfont vendoring, matches what actual enterprise SaaS uses, zero extra assets |

## Architecture

Same Django template inheritance and views/URLs — this is a template + static asset rebuild only.

- **`templates/base.html`** — new shell: fixed slate sidebar for primary nav (Home, Hosts, Firewalls), white top bar with page title + context-aware search, light-gray content area.
- **`static/main/css/theme.css`** (new) — design tokens as CSS custom properties (colors, spacing scale, typography) plus component styles (sidebar, top bar, status badges, `.data-table`, forms, buttons). Loaded after vendored Bootstrap 5 so it can use Bootstrap utility classes and override defaults via variables.
- **Vendored Bootstrap 5 + Popper**, replacing the current 4.5.3 vendor copy, downloaded once from the official distribution (same "local copy, no CDN" pattern already in use for the offline/internal-network deployment).
- **`bootstrap5.modal.forms.js`** (already shipped inside the already-upgraded `django-bootstrap-modal-forms` 3.0.5 package, confirmed vanilla-JS with no jQuery dependency) replaces `jquery.bootstrap.modal.forms.js` for the "Create firewall rule" modal.
- jQuery is removed entirely; the one remaining jQuery usage (`inventory_base.html`'s checkbox-collecting script) is rewritten in vanilla JS.

### Template organization (deduplication)

The current templates hand-duplicate the same markup (status `{% if %}` blocks, table-row form fields) across multiple files with inline styles mixed in. Rather than a SPA/API rewrite, this gets cleaned up with Django's own tools — no new dependencies:

- **Partials** (`templates/partials/`), included via `{% include %}`:
  - `sidebar.html`, `topbar.html` — included once from `base.html`.
  - `form_field.html` — renders one label+input+error block for a given form field; used by every `<form>` template instead of hand-written table rows.
- **Template filter** (`home/templatetags/minitower_extras.py`, new `templatetags` module, loaded with `{% load minitower_extras %}`): `{{ host.server_status|status_badge }}` returns the badge HTML/classes for a status value. One Python function instead of copy-pasted `{% if %}` blocks in `inventory_base.html`, `host_profile.html`, and `firewall_base.html`. Lives in `home` (not `shared_functions`, which is a plain module, not an installed Django app — `{% load %}` only discovers tags from `INSTALLED_APPS`) since the filter is used across both the `inventory` and `firewall` apps and doesn't belong to either one specifically.
- Data tables are **not** forced into a generic reusable partial — each table has different columns, and abstracting that in Django templates would add more indirection than it removes. They stay as individual `<table>` markup sharing the `.data-table` CSS class from `theme.css`.

## Components

- **Sidebar**: logo/wordmark, then nav sections (Home, Hosts → list/add/upload, Firewalls → list/add/upload). Active section highlighted in accent blue.
- **Top bar**: page title on the left; search box on the right, context-aware — posts `host_search` on Hosts pages, `fw_search` on Firewalls pages (reusing the existing `filter()` views in `inventory/views.py` and `firewall/views.py`, no backend changes), hidden on pages without a search-backed view (Home, Upload, Add forms).
- **Data tables**: shared `.data-table` class applied to every raw `<table>` (host list, firewall list, host profile hardware/firewall-connections, fwrule detail) — white background, subtle row dividers, light header instead of solid green `<th>`, hover row highlight. Inline `style="width:..."` attributes removed in favor of CSS.
- **Status badges**: muted pill style (see table above) applied to host up/down status and firewall rule status.
- **Forms**: `add_hosts.html`, `add_firewall.html`, `add_firewallmodal.html`, and both upload templates move from raw `<table>`-row field layout to stacked Bootstrap 5 `.form-label`/`.form-control` fields. Requires adding `attrs={'class': 'form-control'}` to widgets in each app's `forms.py`.
- **Modal**: "Create firewall rule" modal restyled (white modal, slate header text, blue primary button) and rewired to Bootstrap 5's native modal JS via `bootstrap5.modal.forms.js`.
- **Buttons**: one primary style (`.btn-primary`, solid blue) for main actions (Create, Upload, Save); one secondary/outline style for everything else.

## Known bugs fixed while touching these files

- `upload/templates/upload/host-data-upload.html`: `<form method="post" enctype="multipart/form-data"></form>` closes the form tag immediately, so the file input and submit button currently render **outside** the form and the upload button doesn't work from a browser. Fixed as part of the template rewrite.

## Error handling & edge cases

- Django form validation errors restyled as Bootstrap 5 `.is-invalid` / `.invalid-feedback` instead of the current bare `<p class="help-block">`.
- Empty states (no hosts, no firewall rules, no storage devices) get a simple "No results" row instead of rendering a blank table.
- Modal form validation errors continue to work via the ported JS — re-renders the form-with-errors in place, same behavior as the jQuery version.

## Testing

No Python/view/model logic changes, so no new unit tests. Verification is manual, reusing the local venv + dev server setup from the earlier bug-fix pass:
- Hit every page listed in Scope and visually confirm the new shell/theme.
- Exercise both "Create" modals (firewall rule, and confirm host-add form) end-to-end.
- Exercise both upload forms end-to-end (including confirming the fixed host-upload form actually submits from a browser).
- Spot-check in an actual browser (not just `curl`), since this is a visual/JS-behavior change.
