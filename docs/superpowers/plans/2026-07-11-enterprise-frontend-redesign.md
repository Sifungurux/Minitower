# Enterprise Frontend Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild every Minitower template into a sidebar + top-bar enterprise SaaS layout (light corporate gray, blue accent), migrating from Bootstrap 4.5.3 + jQuery to Bootstrap 5 + vanilla JS, with zero URL/view/model changes.

**Architecture:** Django server-rendered templates (unchanged approach). A new `theme.css` design-token stylesheet layered on vendored Bootstrap 5. Three new shared partials (`sidebar.html`, `topbar.html`, `form_field.html`) and one new template filter (`status_badge_class`) eliminate the markup duplication across the 11 existing templates. `django-bootstrap-modal-forms`' first-party `bootstrap5.modal.forms.js` (already present in the installed 3.0.5 package) replaces the jQuery modal-forms script.

**Tech Stack:** Django 4.2 templates, Bootstrap 5.3.3 (vendored, no CDN), vanilla JS, `django-bootstrap-modal-forms` 3.0.5 (already installed).

## Global Constraints

- Vendor all assets locally — no CDN links in any template (matches existing offline/internal-network deployment pattern).
- Drop jQuery entirely; no jQuery file may remain referenced from any template after this plan.
- No Django view, model, or URL changes anywhere in this plan.
- Theme colors (exact values from the spec): sidebar `#2d3340`, sidebar text `#cfd3dc`, top bar `#ffffff` / border `#e2e5ea`, content bg `#f4f5f7`, surface `#ffffff`, body text `#1f2328`, accent `#2f5aad`, accent hover `#24478a`, status-up bg `#e6f4ea` / text `#1e7e34`, status-down bg `#fbe9e9` / text `#b42318`.
- Typography: system font stack `-apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` — no webfont vendoring.
- Sidebar nav items: Home; Hosts → Host list / Add host / Upload hostfile; Firewalls → Firewall rules / Add firewall rule / Upload firewall list.
- Top bar search is context-aware: `host_search` GET param on the host-list page, `fw_search` GET param on the firewall-list page, hidden elsewhere.
- Verification throughout uses the local venv (`.venv/`, Python 3.9, Django 4.2.30) and dev server already set up in this repo — `.venv/bin/python manage.py runserver 127.0.0.1:8765`.

---

## File Structure

**New files:**
- `static/main/css/theme.css` — design tokens + all component styles (sidebar, top bar, data tables, badges, buttons, forms).
- `static/main/js/bootstrap5.modal.forms.js` — vendored copy of the vanilla-JS modal-forms script (from the installed `bootstrap_modal_forms` package).
- `templates/partials/sidebar.html`, `templates/partials/topbar.html`, `templates/partials/form_field.html` — shared includes.
- `home/templatetags/__init__.py`, `home/templatetags/minitower_extras.py` — `status_badge_class` filter.

**Modified files:**
- `static/main/css/bootstrap.css`, `static/main/js/bootstrap.js` — content replaced with Bootstrap 5.3.3.
- `templates/base.html` — new sidebar+topbar shell.
- `home/tests.py` — real test for the new filter.
- `firewall/forms.py` — `widgets` added to `AddModalFirewall.Meta`.
- All 11 page templates listed in the spec, plus `firewall/templates/firewall/add_firewallmodal.html`.

**Deleted files:**
- `static/main/js/jquery-3-6-0.js`, `jquery-3.6.0.min.js`, `jquery.bootstrap.modal.forms.js`, `jquery.bootstrap.modal.forms.min.js`
- `static/main/css/jquery.modal,min.css`, `main.css`, `pd.css`
- `static/main/css/bootstrap-grid.css(.map)`, `bootstrap-grid.min.css(.map)`, `bootstrap-reboot.css(.map)`, `bootstrap-reboot.min.css(.map)`, `bootstrap.css.map`, `bootstrap.min.css`, `bootstrap.min.css.map`
- `static/main/js/bootstrap.bundle.js(.map)`, `bootstrap.bundle.min.js(.map)`, `bootstrap.min.js(.map)`
- `inventory/static/inventory/css/jquery-6-0.js` (unreferenced stray file)

None of the deleted files above are referenced by any template — confirmed by grep during planning.

---

### Task 1: Vendor Bootstrap 5, remove jQuery and unused Bootstrap 4 assets

**Files:**
- Modify: `static/main/css/bootstrap.css`
- Modify: `static/main/js/bootstrap.js`
- Create: `static/main/js/bootstrap5.modal.forms.js`
- Delete: all files listed under "Deleted files" above

**Interfaces:**
- Produces: `{% static 'main/css/bootstrap.css' %}` (Bootstrap 5.3.3 CSS), `{% static 'main/js/bootstrap.js' %}` (Bootstrap 5.3.3 JS, includes the `Modal` component used by Task 10), `{% static 'main/js/bootstrap5.modal.forms.js' %}` exposing a global `modalForm(elem, options)` function (used by Task 10).

- [ ] **Step 1: Download Bootstrap 5.3.3 CSS and JS, overwrite the vendored copies**

```bash
cd /Users/kirk/Development/Minitower
curl -sL "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.css" -o static/main/css/bootstrap.css
curl -sL "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.js" -o static/main/js/bootstrap.js
```

- [ ] **Step 2: Verify the downloads succeeded**

```bash
head -3 static/main/css/bootstrap.css
head -3 static/main/js/bootstrap.js
```

Expected: both show a comment header containing `Bootstrap  v5.3.3`.

- [ ] **Step 3: Vendor the modal-forms vanilla-JS script**

```bash
cp .venv/lib/python3.9/site-packages/bootstrap_modal_forms/static/js/bootstrap5.modal.forms.js static/main/js/bootstrap5.modal.forms.js
```

If `.venv` is not present, reinstall it first: `python3 -m venv .venv && .venv/bin/pip install -r test/requirements.txt`.

- [ ] **Step 4: Delete jQuery and now-unused Bootstrap 4 files**

```bash
rm -f static/main/js/jquery-3-6-0.js static/main/js/jquery-3.6.0.min.js
rm -f static/main/js/jquery.bootstrap.modal.forms.js static/main/js/jquery.bootstrap.modal.forms.min.js
rm -f "static/main/css/jquery.modal,min.css" static/main/css/main.css static/main/css/pd.css
rm -f static/main/css/bootstrap-grid.css static/main/css/bootstrap-grid.css.map
rm -f static/main/css/bootstrap-grid.min.css static/main/css/bootstrap-grid.min.css.map
rm -f static/main/css/bootstrap-reboot.css static/main/css/bootstrap-reboot.css.map
rm -f static/main/css/bootstrap-reboot.min.css static/main/css/bootstrap-reboot.min.css.map
rm -f static/main/css/bootstrap.css.map static/main/css/bootstrap.min.css static/main/css/bootstrap.min.css.map
rm -f static/main/js/bootstrap.bundle.js static/main/js/bootstrap.bundle.js.map
rm -f static/main/js/bootstrap.bundle.min.js static/main/js/bootstrap.bundle.min.js.map
rm -f static/main/js/bootstrap.min.js static/main/js/bootstrap.min.js.map
rm -f inventory/static/inventory/css/jquery-6-0.js
```

- [ ] **Step 5: Confirm nothing else references the deleted files**

```bash
grep -rln "jquery" --include="*.html" . || echo "no jQuery references remain"
```

Expected: `no jQuery references remain` (Task 5 will still reference `bootstrap5.modal.forms.js`, which is not jQuery).

- [ ] **Step 6: Commit**

```bash
git add -A static/main inventory/static/inventory/css
git commit -m "Vendor Bootstrap 5, remove jQuery and unused Bootstrap 4 assets"
```

---

### Task 2: Build the theme.css design system

**Files:**
- Create: `static/main/css/theme.css`

**Interfaces:**
- Produces (CSS classes consumed by every later task): `.app-shell`, `.sidebar`, `.sidebar__brand`, `.sidebar__nav`, `.sidebar__section`, `.sidebar__link`, `.sidebar__link--active`, `.main`, `.topbar`, `.topbar__title`, `.topbar__search`, `.content`, `.site-footer`, `.card`, `.data-table`, `.data-table__empty`, `.status-badge`, `.status-badge--up`, `.status-badge--down`.

- [ ] **Step 1: Create the file**

```css
:root {
  --color-sidebar-bg: #2d3340;
  --color-sidebar-text: #cfd3dc;
  --color-sidebar-text-muted: #8b93a7;
  --color-accent: #2f5aad;
  --color-accent-hover: #24478a;
  --color-topbar-bg: #ffffff;
  --color-topbar-border: #e2e5ea;
  --color-content-bg: #f4f5f7;
  --color-surface: #ffffff;
  --color-text: #1f2328;
  --color-text-muted: #6b7280;
  --color-border: #e2e5ea;
  --status-up-bg: #e6f4ea;
  --status-up-text: #1e7e34;
  --status-down-bg: #fbe9e9;
  --status-down-text: #b42318;
  --font-sans: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --radius: 6px;
  --sidebar-width: 240px;
  --topbar-height: 56px;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: var(--font-sans);
  color: var(--color-text);
  background: var(--color-content-bg);
}

a { color: var(--color-accent); text-decoration: none; }
a:hover { color: var(--color-accent-hover); text-decoration: underline; }

/* Layout shell */
.app-shell { display: flex; min-height: 100vh; }

.sidebar {
  width: var(--sidebar-width);
  background: var(--color-sidebar-bg);
  color: var(--color-sidebar-text);
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  padding: var(--space-md) 0;
  overflow-y: auto;
}

.sidebar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: 0 var(--space-md) var(--space-lg);
  color: #ffffff;
  font-weight: 600;
  font-size: 1.05rem;
}

.sidebar__brand img { border-radius: 4px; }

.sidebar__nav { display: flex; flex-direction: column; }

.sidebar__section {
  padding: var(--space-md) var(--space-md) var(--space-xs);
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-sidebar-text-muted);
}

.sidebar__link {
  display: block;
  padding: var(--space-sm) var(--space-md);
  color: var(--color-sidebar-text);
  border-left: 3px solid transparent;
}

.sidebar__link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
  text-decoration: none;
}

.sidebar__link--active {
  background: rgba(47, 90, 173, 0.25);
  color: #ffffff;
  border-left-color: var(--color-accent);
  font-weight: 600;
}

.main {
  margin-left: var(--sidebar-width);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: var(--topbar-height);
  min-height: var(--topbar-height);
  background: var(--color-topbar-bg);
  border-bottom: 1px solid var(--color-topbar-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-lg);
}

.topbar__title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0;
  color: var(--color-text);
}

.topbar__search { margin: 0; }
.topbar__search input { width: 260px; }

.content { flex: 1; padding: var(--space-lg); }

.site-footer {
  padding: var(--space-md) var(--space-lg);
  color: var(--color-text-muted);
  font-size: 0.8rem;
  border-top: 1px solid var(--color-border);
  background: var(--color-topbar-bg);
}

/* Cards */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
}

/* Data tables */
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
}

.data-table th {
  background: var(--color-content-bg);
  color: var(--color-text-muted);
  text-transform: uppercase;
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-align: left;
  padding: var(--space-sm) var(--space-md);
  border-bottom: 2px solid var(--color-border);
}

.data-table td {
  padding: var(--space-sm) var(--space-md);
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.data-table tbody tr:hover { background: var(--color-content-bg); }
.data-table tbody tr:last-child td { border-bottom: none; }

.data-table__empty {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--space-lg);
}

/* Status badges */
.status-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.72rem;
  font-weight: 600;
}

.status-badge--up { background: var(--status-up-bg); color: var(--status-up-text); }
.status-badge--down { background: var(--status-down-bg); color: var(--status-down-text); }

/* Buttons */
.btn-primary {
  background-color: var(--color-accent);
  border-color: var(--color-accent);
}
.btn-primary:hover,
.btn-primary:focus {
  background-color: var(--color-accent-hover);
  border-color: var(--color-accent-hover);
}

/* Forms */
.form-label { font-weight: 600; font-size: 0.85rem; color: var(--color-text); }
.invalid-feedback.d-block { color: var(--status-down-text); font-size: 0.8rem; }
```

- [ ] **Step 2: Verify no obvious syntax errors**

```bash
python3 -c "
content = open('static/main/css/theme.css').read()
assert content.count('{') == content.count('}'), 'unbalanced braces'
print('OK, braces balanced:', content.count('{'))
"
```

Expected: `OK, braces balanced: <some number>` with no `AssertionError`.

- [ ] **Step 3: Commit**

```bash
git add static/main/css/theme.css
git commit -m "Add theme.css design system for enterprise redesign"
```

---

### Task 3: Add the `status_badge_class` template filter

**Files:**
- Create: `home/templatetags/__init__.py`
- Create: `home/templatetags/minitower_extras.py`
- Modify: `home/tests.py`

**Interfaces:**
- Consumes: nothing (pure function).
- Produces: `status_badge_class(value: str) -> str`, returning `"status-badge--up"` or `"status-badge--down"`. Loaded in templates via `{% load minitower_extras %}` then `{{ value|status_badge_class }}`. Used by Task 7 (`inventory_base.html`) and Task 10 (`firewall_base.html`).

- [ ] **Step 1: Write the failing test**

Replace the contents of `home/tests.py`:

```python
from django.test import TestCase

from home.templatetags.minitower_extras import status_badge_class


class StatusBadgeClassFilterTests(TestCase):
    def test_connected_is_up(self):
        self.assertEqual(status_badge_class("Connected"), "status-badge--up")

    def test_case_insensitive(self):
        self.assertEqual(status_badge_class("ACTIVE"), "status-badge--up")

    def test_unknown_value_is_down(self):
        self.assertEqual(status_badge_class("Disconnected"), "status-badge--down")

    def test_empty_value_is_down(self):
        self.assertEqual(status_badge_class(""), "status-badge--down")

    def test_none_value_is_down(self):
        self.assertEqual(status_badge_class(None), "status-badge--down")
```

- [ ] **Step 2: Run it to verify it fails**

```bash
.venv/bin/python -m pytest home/tests.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'home.templatetags'`.

- [ ] **Step 3: Create the templatetags module**

```bash
mkdir -p home/templatetags
touch home/templatetags/__init__.py
```

`home/templatetags/minitower_extras.py`:

```python
from django import template

register = template.Library()

UP_VALUES = {"connected", "up", "active"}


@register.filter
def status_badge_class(value):
    if str(value).strip().lower() in UP_VALUES:
        return "status-badge--up"
    return "status-badge--down"
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
.venv/bin/python -m pytest home/tests.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add home/templatetags home/tests.py
git commit -m "Add status_badge_class template filter with tests"
```

---

### Task 4: Build shared partials (sidebar, top bar, form field)

**Files:**
- Create: `templates/partials/sidebar.html`
- Create: `templates/partials/topbar.html`
- Create: `templates/partials/form_field.html`

**Interfaces:**
- Consumes: Django's `request` context processor (already enabled in `minitower/settings.py`'s `TEMPLATES[0]['OPTIONS']['context_processors']`), URL names `home`, `index`, `profile`, `add_host_create`, `hostdata_upload`, `get_firewall_list`, `get_fwrule`, `add_fw_create`, `fwdata_upload` (all already registered — verified against `home/urls.py`, `inventory/urls.py`, `hosts/urls.py`, `firewall/urls.py`, `upload/urls.py`), and the `title` context variable most views already pass.
- Produces: `{% include 'partials/sidebar.html' %}`, `{% include 'partials/topbar.html' %}` (both used by Task 5's `base.html`), and `{% include 'partials/form_field.html' with field=form.somefield %}` (used by Tasks 9, 12, 13).

- [ ] **Step 1: Create the sidebar partial**

`templates/partials/sidebar.html`:

```html
{% load static %}
<aside class="sidebar">
  <a class="sidebar__brand" href="{% url 'home' %}">
    <img src="{% static 'home/img/tower.jpg' %}" width="24" height="24" alt="Minitower">
    <span>Minitower</span>
  </a>
  <nav class="sidebar__nav">
    {% with url_name=request.resolver_match.url_name %}
    <a class="sidebar__link{% if url_name == 'home' %} sidebar__link--active{% endif %}" href="{% url 'home' %}">Home</a>

    <div class="sidebar__section">Hosts</div>
    <a class="sidebar__link{% if url_name == 'index' or url_name == 'profile' %} sidebar__link--active{% endif %}" href="{% url 'index' %}">Host list</a>
    <a class="sidebar__link{% if url_name == 'add_host_create' %} sidebar__link--active{% endif %}" href="{% url 'add_host_create' %}">Add host</a>
    <a class="sidebar__link{% if url_name == 'hostdata_upload' %} sidebar__link--active{% endif %}" href="{% url 'hostdata_upload' %}">Upload hostfile</a>

    <div class="sidebar__section">Firewalls</div>
    <a class="sidebar__link{% if url_name == 'get_firewall_list' or url_name == 'get_fwrule' %} sidebar__link--active{% endif %}" href="{% url 'get_firewall_list' %}">Firewall rules</a>
    <a class="sidebar__link{% if url_name == 'add_fw_create' %} sidebar__link--active{% endif %}" href="{% url 'add_fw_create' %}">Add firewall rule</a>
    <a class="sidebar__link{% if url_name == 'fwdata_upload' %} sidebar__link--active{% endif %}" href="{% url 'fwdata_upload' %}">Upload firewall list</a>
    {% endwith %}
  </nav>
</aside>
```

This also fixes two dead links from the old navbar: "Add host" used to hard-code `href="/inventory/add-host/"` (404 — the real route is `/add-host/`) and "Add firewall rule" hard-coded `href="/firewall/add-firewall/"` (404 — the real route is `/add-firewall/`). Using `{% url %}` here fixes both.

- [ ] **Step 2: Create the top bar partial**

`templates/partials/topbar.html`:

```html
<header class="topbar">
  <h1 class="topbar__title">{{ title|default:"Minitower" }}</h1>
  {% with url_name=request.resolver_match.url_name %}
    {% if url_name == 'index' %}
    <form class="topbar__search" method="get" action="{% url 'index' %}">
      <input type="search" name="host_search" class="form-control form-control-sm" placeholder="Search hosts" value="{{ request.GET.host_search }}">
    </form>
    {% elif url_name == 'get_firewall_list' %}
    <form class="topbar__search" method="get" action="{% url 'get_firewall_list' %}">
      <input type="search" name="fw_search" class="form-control form-control-sm" placeholder="Search firewall rules" value="{{ request.GET.fw_search }}">
    </form>
    {% endif %}
  {% endwith %}
</header>
```

- [ ] **Step 3: Create the form field partial**

`templates/partials/form_field.html`:

```html
<div class="mb-3">
  <label for="{{ field.id_for_label }}" class="form-label">{{ field.label }}</label>
  {{ field }}
  {% if field.errors %}
  <div class="invalid-feedback d-block">{{ field.errors|join:", " }}</div>
  {% endif %}
</div>
```

- [ ] **Step 4: Verify Django can find the partials directory**

```bash
.venv/bin/python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minitower.settings')
django.setup()
from django.template.loader import get_template
get_template('partials/sidebar.html')
get_template('partials/topbar.html')
get_template('partials/form_field.html')
print('all partials resolve')
"
```

Expected: `all partials resolve` with no `TemplateDoesNotExist`.

- [ ] **Step 5: Commit**

```bash
git add templates/partials
git commit -m "Add shared sidebar, topbar, and form_field partials"
```

---

### Task 5: Rebuild base.html shell

**Files:**
- Modify: `templates/base.html`

**Interfaces:**
- Consumes: `templates/partials/sidebar.html`, `templates/partials/topbar.html` (Task 4), `static/main/css/bootstrap.css`, `static/main/css/theme.css` (Task 2), `static/main/js/bootstrap.js`, `static/main/js/bootstrap5.modal.forms.js` (Task 1).
- Produces: `{% block title %}`, `{% block content %}`, `{% block extra_js %}` — the three blocks every page template overrides, matching the child templates written in Tasks 6–15.

- [ ] **Step 1: Replace the file contents**

```html
{% load static %}
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}{{ title|default:"Minitower" }}{% endblock title %}</title>
  <link href="{% static 'main/css/bootstrap.css' %}" rel="stylesheet" type="text/css">
  <link href="{% static 'main/css/theme.css' %}" rel="stylesheet" type="text/css">
</head>
<body>
  <div class="app-shell">
    {% include 'partials/sidebar.html' %}
    <div class="main">
      {% include 'partials/topbar.html' %}
      <div class="content">
        {% block content %}
        <p>Placeholder text in base template. Replace with page content.</p>
        {% endblock content %}
      </div>
      <footer class="site-footer">
        Copyright &copy; <span id="copyright-year"></span> Minitower — Made by System team 4
      </footer>
    </div>
  </div>

  <script src="{% static 'main/js/bootstrap.js' %}"></script>
  <script src="{% static 'main/js/bootstrap5.modal.forms.js' %}"></script>
  <script>
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
  </script>
  {% block extra_js %}{% endblock extra_js %}
</body>
</html>
```

- [ ] **Step 2: Start the dev server and verify the shell renders**

```bash
rm -f db.sqlite3
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8765 > /tmp/minitower-dev.log 2>&1 &
sleep 2
curl -s http://127.0.0.1:8765/ | grep -o 'class="app-shell"\|class="sidebar"\|class="topbar"'
```

Expected: all three classes printed (page loads with the new shell even though `home/index.html` hasn't been rewritten yet — it still uses the old `<H1>` markup from inside the new `{% block content %}`, which is fine at this stage).

Leave this server running — every verification step in Tasks 6 through 15 curls `http://127.0.0.1:8765` against this same running instance. Only Task 16 Step 4 stops it.

- [ ] **Step 3: Commit**

```bash
git add templates/base.html
git commit -m "Rebuild base.html with sidebar + topbar shell"
```

---

### Task 6: Rewrite home/index.html and home/about.html

**Files:**
- Modify: `home/templates/home/index.html`
- Modify: `home/templates/home/about.html`

**Interfaces:**
- Consumes: `base.html` blocks from Task 5.

- [ ] **Step 1: Rewrite index.html**

`home/templates/home/index.html`:

```html
{% extends 'base.html' %}
{% block content %}
<div class="card" style="text-align:center">
  <h2 style="margin-bottom:4px">Minitower</h2>
  <p style="color:var(--color-text-muted)">Home of everything.</p>
</div>
{% endblock content %}
```

The old page-filling `tower.jpg` hero image is dropped — the logo already appears in the sidebar brand, and a large photo doesn't fit the enterprise-dashboard look.

- [ ] **Step 2: Rewrite about.html**

`home/templates/home/about.html`:

```html
{% extends 'base.html' %}
{% block content %}
<div class="card">
  <p>Minitower is an internal inventory, firewall and configuration tracking tool.</p>
</div>
{% endblock content %}
```

- [ ] **Step 3: Verify both pages**

```bash
curl -s -o /dev/null -w "home: %{http_code}\n" http://127.0.0.1:8765/
curl -s -o /dev/null -w "about: %{http_code}\n" http://127.0.0.1:8765/about/
```

Expected: both `200`.

- [ ] **Step 4: Commit**

```bash
git add home/templates/home/index.html home/templates/home/about.html
git commit -m "Restyle home and about pages"
```

---

### Task 7: Rewrite inventory_base.html (host list)

**Files:**
- Modify: `inventory/templates/inventory/inventory_base.html`

**Interfaces:**
- Consumes: `status_badge_class` filter (Task 3), `.data-table`/`.status-badge` CSS (Task 2).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% load static %}
{% load minitower_extras %}

{% block content %}
<form method="post" action="">
  {% csrf_token %}
  <div class="card">
    <table class="data-table" id="hosttable">
      <thead>
        <tr>
          <th style="width:32px"><input type="checkbox" value="all"></th>
          <th>Hostname</th>
          <th style="width:48px">OS</th>
          <th>System</th>
          <th>Server type</th>
          <th>Version</th>
          <th>Status</th>
          <th>Connection</th>
        </tr>
      </thead>
      <tbody>
        {% for host in queryset %}
        <tr>
          <td><input type="checkbox" value="{{ host.host }}" class="hostname"></td>
          <td><a href="{% url 'profile' host.host %}">{{ host.host }}</a></td>
          {% if host.system == "Linux" %}
          <td><img src="{% static 'inventory/img/redhat.png' %}" width="24" height="24" alt="Linux"></td>
          {% elif host.system == "Windows" %}
          <td><img src="{% static 'inventory/img/Windows.png' %}" width="24" height="24" alt="Windows"></td>
          {% else %}
          <td><img src="{% static 'inventory/img/RDP.png' %}" width="24" height="24" alt="ssh"></td>
          {% endif %}
          <td>{{ host.host.systemproduct }}</td>
          <td>{{ host.host.systemtype }}</td>
          <td>{{ host.os_version }}</td>
          <td><span class="status-badge {{ host.host.server_status|status_badge_class }}">{{ host.host.server_status }}</span></td>
          <td>{% if host.host.connectiontype == 22 %}SSH{% elif host.host.connectiontype == 5985 %}KERBEROS{% endif %}</td>
        </tr>
        {% empty %}
        <tr><td colspan="8" class="data-table__empty">No hosts found.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
  <div class="mt-3">
    <input type="submit" id="hostnamevalues" name="hostnames" value="Generate Report" class="btn btn-primary">
  </div>
</form>
{% endblock content %}

{% block extra_js %}
<script>
  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.hostname').forEach(function (checkbox) {
      checkbox.addEventListener('change', function () {
        var selected = Array.prototype.slice.call(document.querySelectorAll('.hostname:checked'))
          .map(function (cb) { return cb.value; })
          .join(',');
        document.getElementById('hostnamevalues').value = selected;
      });
    });
  });
</script>
{% endblock extra_js %}
```

This is a 1:1 behavioral port of the old jQuery checkbox-collector (same `id="hostnamevalues"`/`name="hostnames"` quirk the view already expects) to vanilla JS — no functional change, just no jQuery.

- [ ] **Step 2: Verify against a real host row**

```bash
.venv/bin/python manage.py shell -c "
from hosts.models import hosts
hosts.objects.get_or_create(hostname='uitest01.example.com', defaults=dict(description='d', systemproduct='p', systemtype='t', server_status='Connected', environment='prod', connectiontype=22, vendor='dell', supplier='acme'))
"
curl -s http://127.0.0.1:8765/inventory/ | grep -o 'status-badge--up\|data-table'
```

Expected: both `data-table` and `status-badge--up` present (host has `server_status='Connected'`).

- [ ] **Step 3: Commit**

```bash
git add inventory/templates/inventory/inventory_base.html
git commit -m "Restyle host list page with data-table and status badges"
```

---

### Task 8: Rewrite host_profile.html

**Files:**
- Modify: `inventory/templates/inventory/host_profile.html`

**Interfaces:**
- Consumes: `.card`/`.data-table` CSS (Task 2). No filter needed here — firewall connections keep plain text status per the original page (only the host-list and firewall-list pages get badges, matching Task 7 and Task 10).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="card">
  {% for host in hosts %}
  <div><strong>System:</strong> {{ host.systemtype }}</div>
  <div><strong>Supplier:</strong> {{ host.supplier }}</div>
  <div><strong>Platform:</strong> {{ host.vendor }}</div>
  {% endfor %}
  {% for host in hostHW %}
  <div><strong>OS:</strong> {{ host.os_family }} {{ host.os_version }}</div>
  <div><strong>IP:</strong> {{ host.ip }}</div>
  {% endfor %}
</div>

<div class="card">
  <h2 class="h6">Hardware</h2>
  <table class="data-table">
    <tbody>
      <tr>
        <td style="width:40px"><img src="{% static 'inventory/img/computer-drive-clipart-2.jpg' %}" width="24" height="24" alt="Storage"></td>
        {% for s in storage %}
        <td>{{ s.name }} : {{ s.size }} GB</td>
        {% endfor %}
      </tr>
      {% for host in hostHW %}
      <tr>
        <td><img src="{% static 'inventory/img/memory.png' %}" width="24" height="24" alt="RAM"></td>
        <td>{{ host.ram }} MB</td>
      </tr>
      <tr>
        <td><img src="{% static 'inventory/img/cpu.png' %}" width="24" height="24" alt="CPU"></td>
        <td>{{ host.cores }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
</div>

<div class="card">
  <h2 class="h6">Firewall connections</h2>
  <table class="data-table">
    <thead>
      <tr>
        <th>Fw id</th>
        <th>Reference id</th>
        <th>Source</th>
        <th>Destination</th>
        <th>Port</th>
        <th>Protocol</th>
        <th>Status</th>
        <th>Ticket nr.</th>
        <th>Description/Note</th>
      </tr>
    </thead>
    <tbody>
      {% for fw in fwset %}
      <tr>
        <td><a href="{% url 'get_fwrule' fw.id %}">{{ fw.id }}</a></td>
        <td>{{ fw.ref }}</td>
        <td>{{ fw.source }}</td>
        <td>{{ fw.dest }}</td>
        <td>{{ fw.port }}</td>
        <td>{{ fw.protocol }}</td>
        <td>{{ fw.status }}</td>
        <td>{{ fw.ticket }}</td>
        <td>{{ fw.description }}<br>{{ fw.note }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="9" class="data-table__empty">No firewall connections found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock content %}
```

This also fixes a structural bug found while reading the original: the old template opened `{% for host in hostHW %}` around the supplier/platform block and never closed it until deep inside the hardware table (spanning the entire aqua-placeholder `<td>` and the whole hardware section). It happened to render correctly only because `hostHW` always has exactly one row per host. This rewrite uses correctly-scoped, independent loops with identical output for that one-row case. The empty `style="background-color: aqua"` placeholder `<div>` is also dropped (it rendered nothing — pure dead markup).

- [ ] **Step 2: Verify against the fixture host**

```bash
curl -s http://127.0.0.1:8765/profile/uitest01.example.com | grep -o 'data-table\|Supplier\|Platform'
```

Expected: `data-table`, `Supplier`, `Platform` all present.

- [ ] **Step 3: Commit**

```bash
git add inventory/templates/inventory/host_profile.html
git commit -m "Restyle host profile page, fix unclosed loop and dead aqua placeholder"
```

---

### Task 9: Rewrite hosts/add_hosts.html

**Files:**
- Modify: `hosts/templates/hosts/add_hosts.html`

**Interfaces:**
- Consumes: `partials/form_field.html` (Task 4). `hosts/forms.py`'s `AddHost` fields already carry `class: 'form-control'` (verified during planning — no `forms.py` change needed here).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% block content %}
<div class="card" style="max-width:600px">
  <form method="post" action=".">
    {% csrf_token %}
    {% include 'partials/form_field.html' with field=form.hostname %}
    {% include 'partials/form_field.html' with field=form.systemproduct %}
    {% include 'partials/form_field.html' with field=form.system_owner %}
    {% include 'partials/form_field.html' with field=form.environment %}
    {% include 'partials/form_field.html' with field=form.description %}
    <button type="submit" class="btn btn-primary">Save</button>
  </form>
</div>
{% endblock content %}
```

- [ ] **Step 2: Verify the form renders**

```bash
curl -s http://127.0.0.1:8765/add-host/ | grep -o 'form-control\|form-label' | sort | uniq -c
```

Expected: both `form-control` and `form-label` present multiple times (once per field).

- [ ] **Step 3: Commit**

```bash
git add hosts/templates/hosts/add_hosts.html
git commit -m "Restyle add-host form using form_field partial"
```

---

### Task 10: Rewrite firewall_base.html (firewall list + modal trigger)

**Files:**
- Modify: `firewall/templates/firewall/firewall_base.html`

**Interfaces:**
- Consumes: `status_badge_class` filter (Task 3), `modalForm(elem, options)` global from `bootstrap5.modal.forms.js` (Task 1), URL name `create_firewall_rule` (already registered in `firewall/urls.py`).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% load static %}
{% load minitower_extras %}

{% block content %}
<div class="mb-3">
  <button id="create-firewall-rule" class="btn btn-primary" type="button">Create firewall rule</button>
</div>

<div class="card">
  <table class="data-table">
    <thead>
      <tr>
        <th>Fw id</th>
        <th>Reference id</th>
        <th>Source</th>
        <th>Destination</th>
        <th>Port</th>
        <th>Protocol</th>
        <th>Status</th>
        <th>Ticket nr.</th>
        <th>Description/Note</th>
      </tr>
    </thead>
    <tbody>
      {% for fw in queryset %}
      <tr>
        <td><a href="{% url 'get_fwrule' fw.id %}">{{ fw.id }}</a></td>
        <td>{{ fw.ref }}</td>
        <td>{{ fw.source }}</td>
        <td>{{ fw.dest }}</td>
        <td>{{ fw.port }}</td>
        <td>{{ fw.protocol }}</td>
        <td><span class="status-badge {{ fw.status|status_badge_class }}">{{ fw.status }}</span></td>
        <td>{{ fw.ticket }}</td>
        <td>{{ fw.description }}<br>{{ fw.note }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="9" class="data-table__empty">No firewall rules found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>

<div class="modal fade" id="modal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content"></div>
  </div>
</div>
{% endblock content %}

{% block extra_js %}
<script>
  document.addEventListener('DOMContentLoaded', function () {
    modalForm(document.getElementById('create-firewall-rule'), {
      formURL: "{% url 'create_firewall_rule' %}"
    });
  });
</script>
{% endblock extra_js %}
```

- [ ] **Step 2: Verify the page and modal trigger markup**

```bash
curl -s http://127.0.0.1:8765/firewall/ | grep -o 'id="create-firewall-rule"\|id="modal"\|data-table'
```

Expected: all three present.

- [ ] **Step 3: Commit**

```bash
git add firewall/templates/firewall/firewall_base.html
git commit -m "Restyle firewall list page, port modal trigger to vanilla JS"
```

---

### Task 11: Rewrite fwrule.html (firewall rule detail)

**Files:**
- Modify: `firewall/templates/firewall/fwrule.html`

**Interfaces:**
- Consumes: `.data-table` CSS (Task 2).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}

{% block content %}
<div class="card">
  <table class="data-table">
    <thead>
      <tr>
        <th>Fw id</th>
        <th>Reference id</th>
        <th>Source</th>
        <th>Source NAT</th>
        <th>Destination</th>
        <th>Destination NAT</th>
        <th>Port</th>
        <th>Protocol</th>
        <th>Status</th>
        <th>Ticket nr.</th>
        <th>Description/Note</th>
      </tr>
    </thead>
    <tbody>
      {% for fw in fwset %}
      <tr>
        <td>{{ fw.id }}</td>
        <td>{{ fw.ref }}</td>
        <td>{{ fw.source }}</td>
        <td>{{ fw.sourcenat }}</td>
        <td>{{ fw.dest }}</td>
        <td>{{ fw.destnat }}</td>
        <td>{{ fw.port }}</td>
        <td>{{ fw.protocol }}</td>
        <td>{{ fw.status }}</td>
        <td>{{ fw.ticket }}</td>
        <td>{{ fw.description }}<br>{{ fw.note }}</td>
      </tr>
      {% empty %}
      <tr><td colspan="11" class="data-table__empty">Rule not found.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock content %}
```

- [ ] **Step 2: Verify against a real rule**

```bash
.venv/bin/python manage.py shell -c "
from firewall.models import firewall
fw, _ = firewall.objects.get_or_create(source='10.0.0.1', dest='10.0.0.2', port='443', defaults=dict(sourcenat='-', destnat='-', protocol='tcp', ref='REF-UI', ticket='TCK1', description='ui test', status='active', note=''))
print(fw.id)
"
curl -s http://127.0.0.1:8765/fwrule/1 | grep -o 'data-table'
```

Expected: `data-table` present.

- [ ] **Step 3: Commit**

```bash
git add firewall/templates/firewall/fwrule.html
git commit -m "Restyle firewall rule detail page"
```

---

### Task 12: Rewrite add_firewall.html

**Files:**
- Modify: `firewall/templates/firewall/add_firewall.html`

**Interfaces:**
- Consumes: `partials/form_field.html` (Task 4). `firewall/forms.py`'s `AddFirewall` fields already carry `class: 'form-control'` (verified during planning — no `forms.py` change needed for this form; Task 13 handles the separate `AddModalFirewall` form).

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% block content %}
<div class="card" style="max-width:800px">
  <form method="post" action=".">
    {% csrf_token %}
    <div class="row">
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.source %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.sourcenat %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.dest %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.destnat %}</div>
    </div>
    <div class="row">
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.port %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.protocol %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.ref %}</div>
      <div class="col-md-3">{% include 'partials/form_field.html' with field=form.ticket %}</div>
    </div>
    <div class="row">
      <div class="col-md-6">{% include 'partials/form_field.html' with field=form.status %}</div>
    </div>
    <div class="row">
      <div class="col-md-6">{% include 'partials/form_field.html' with field=form.note %}</div>
      <div class="col-md-6">{% include 'partials/form_field.html' with field=form.description %}</div>
    </div>

    {% if form.source.value %}
    <div class="card" style="background:var(--color-content-bg)">
      <strong>
        {% if form.sourcenat.value %}
          {{ form.source.value }} from {{ form.sourcenat.value }} via {{ form.destnat.value }}:{{ form.port.value }} to {{ form.dest.value }}
        {% else %}
          {{ form.source.value }} to {{ form.dest.value }}:{{ form.port.value }}
        {% endif %}
      </strong>
    </div>
    {% endif %}

    <button type="submit" name="validate" value="Validate" class="btn btn-primary">Validate</button>
  </form>
</div>
{% endblock content %}
```

The old picture-based "src → dest" flow diagram referenced two images that don't exist on disk (`firewall/img/right-arrow.jpg`, `firewall/img/cloud.png` — confirmed missing via `firewall/static/firewall/` listing during planning, so those `<img>` tags have always 404'd) and had a duplicated identical `{% if form.sourcenat.value == '' %}` condition nested inside itself. Both are replaced by the single text summary line above, which preserves the only real information the diagram conveyed.

- [ ] **Step 2: Verify the form renders**

```bash
curl -s http://127.0.0.1:8765/add-firewall/ | grep -o 'form-control' | wc -l
```

Expected: a number greater than 0 (one per field).

- [ ] **Step 3: Commit**

```bash
git add firewall/templates/firewall/add_firewall.html
git commit -m "Restyle add-firewall form, drop broken image diagram and duplicated condition"
```

---

### Task 13: Style AddModalFirewall widgets and rewrite the modal template

**Files:**
- Modify: `firewall/forms.py`
- Modify: `firewall/templates/firewall/add_firewallmodal.html`

**Interfaces:**
- Consumes: `partials/form_field.html` (Task 4).
- Produces: `AddModalFirewall` widgets now carry `class: 'form-control'` (previously bare, since `BSModalModelForm` — verified in the installed package source — does not auto-apply Bootstrap classes).

- [ ] **Step 1: Add widgets to AddModalFirewall.Meta**

In `firewall/forms.py`, replace:

```python
class AddModalFirewall(BSModalModelForm):
    class Meta:
        model = firewall
        fields = ['source', 'sourcenat','dest', 'destnat', 'port', 'protocol', 'ref','ticket', 'description']
```

with:

```python
class AddModalFirewall(BSModalModelForm):
    class Meta:
        model = firewall
        fields = ['source', 'sourcenat', 'dest', 'destnat', 'port', 'protocol', 'ref', 'ticket', 'description']
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'sourcenat': forms.TextInput(attrs={'class': 'form-control'}),
            'dest': forms.TextInput(attrs={'class': 'form-control'}),
            'destnat': forms.TextInput(attrs={'class': 'form-control'}),
            'port': forms.TextInput(attrs={'class': 'form-control'}),
            'protocol': forms.TextInput(attrs={'class': 'form-control'}),
            'ref': forms.TextInput(attrs={'class': 'form-control'}),
            'ticket': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
```

- [ ] **Step 2: Rewrite the modal template**

`firewall/templates/firewall/add_firewallmodal.html` (rendered as an AJAX fragment injected into `.modal-content` — must NOT extend `base.html`):

```html
<form method="post" action="">
  {% csrf_token %}
  <div class="modal-header">
    <h5 class="modal-title">Create Firewall rule</h5>
    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
  </div>
  <div class="modal-body">
    {% include 'partials/form_field.html' with field=form.source %}
    {% include 'partials/form_field.html' with field=form.sourcenat %}
    {% include 'partials/form_field.html' with field=form.dest %}
    {% include 'partials/form_field.html' with field=form.destnat %}
    {% include 'partials/form_field.html' with field=form.port %}
    {% include 'partials/form_field.html' with field=form.protocol %}
    {% include 'partials/form_field.html' with field=form.ref %}
    {% include 'partials/form_field.html' with field=form.ticket %}
    {% include 'partials/form_field.html' with field=form.description %}
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
    <button type="submit" class="btn btn-primary">Create</button>
  </div>
</form>
```

Note the Bootstrap 5 attribute/markup changes from the old Bootstrap 4 version: `data-dismiss` → `data-bs-dismiss`, and the close button changed from `<button class="close"><span aria-hidden="true">&times;</span></button>` to `<button class="btn-close" aria-label="Close"></button>`.

- [ ] **Step 3: Verify the modal fragment renders standalone (not through base.html)**

```bash
curl -s http://127.0.0.1:8765/create/ | grep -o 'modal-header\|form-control' | sort | uniq -c
```

Expected: `modal-header` once, `form-control` nine times (one per field). No `<html>`/`<body>` tags in the output (confirms it did not accidentally extend `base.html`).

- [ ] **Step 4: Commit**

```bash
git add firewall/forms.py firewall/templates/firewall/add_firewallmodal.html
git commit -m "Style AddModalFirewall widgets, port modal fragment to Bootstrap 5 markup"
```

---

### Task 14: Rewrite upload/host-data-upload.html (and fix the broken form tag)

**Files:**
- Modify: `upload/templates/upload/host-data-upload.html`

**Interfaces:**
- None — self-contained page.

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% block content %}
<div class="card" style="max-width:600px">
  <form method="post" enctype="multipart/form-data" action="">
    {% csrf_token %}
    <div class="mb-3">
      <input type="file" name="systemdata" class="form-control">
    </div>
    <button type="submit" class="btn btn-primary">Upload</button>
  </form>

  {% if uploaded_file_url %}
  <p class="mt-3">File uploaded at: <a href="{{ uploaded_file_url }}">{{ uploaded_file_url }}</a></p>
  {% endif %}

  {% for error in msg %}
  <p class="mt-2">{{ error }}</p>
  {% endfor %}

  <a href="{% url 'home' %}">Return to home</a>
</div>
{% endblock content %}
```

This fixes the bug found while reading the original template: it wrote `<form method="post" enctype="multipart/form-data"></form>` — closing the form tag immediately — so the `{% csrf_token %}`, file input, and submit button all rendered **outside** the form and the upload button has never worked from a browser (only direct POST requests, like the ones used in earlier manual testing, exercised the view).

- [ ] **Step 2: Verify the fix — the input must now be inside the form**

```bash
curl -s http://127.0.0.1:8765/inventory/upload/ | python3 -c "
import sys, re
html = sys.stdin.read()
form_match = re.search(r'<form.*?</form>', html, re.DOTALL)
assert form_match, 'no form found'
assert 'name=\"systemdata\"' in form_match.group(0), 'file input is outside the form'
print('OK: file input is inside the form')
"
```

Expected: `OK: file input is inside the form`.

- [ ] **Step 3: Commit**

```bash
git add upload/templates/upload/host-data-upload.html
git commit -m "Restyle host upload page, fix form tag closed before its inputs"
```

---

### Task 15: Rewrite upload/fw-data-upload.html (same broken-form-tag bug)

**Files:**
- Modify: `upload/templates/upload/fw-data-upload.html`

**Interfaces:**
- None — self-contained page.

- [ ] **Step 1: Replace the file contents**

```html
{% extends 'base.html' %}
{% block content %}
<div class="card" style="max-width:600px">
  <form method="post" enctype="multipart/form-data" action="">
    {% csrf_token %}
    <div class="mb-3">
      <input type="file" name="fwdata" class="form-control">
    </div>
    <button type="submit" class="btn btn-primary">Upload</button>
  </form>

  {% if uploaded_file_url %}
  <p class="mt-3">File uploaded at: <a href="{{ uploaded_file_url }}">{{ uploaded_file_url }}</a></p>
  {% endif %}

  {% for error in msg %}
  <p class="mt-2">{{ error }}</p>
  {% endfor %}

  <a href="{% url 'home' %}">Return to home</a>
</div>
{% endblock content %}
```

This is the same "form closed before its inputs" bug as Task 14, found in this sibling template during planning (`upload/templates/upload/fw-data-upload.html` had the identical `<form ...></form>` typo) — fixed the same way.

- [ ] **Step 2: Verify the fix**

```bash
curl -s http://127.0.0.1:8765/firewall/upload/ | python3 -c "
import sys, re
html = sys.stdin.read()
form_match = re.search(r'<form.*?</form>', html, re.DOTALL)
assert form_match, 'no form found'
assert 'name=\"fwdata\"' in form_match.group(0), 'file input is outside the form'
print('OK: file input is inside the form')
"
```

Expected: `OK: file input is inside the form`.

- [ ] **Step 3: Commit**

```bash
git add upload/templates/upload/fw-data-upload.html
git commit -m "Restyle firewall upload page, fix form tag closed before its inputs"
```

---

### Task 16: Full manual smoke test

**Files:** none (verification only).

**Interfaces:** none.

- [ ] **Step 1: Run the automated test suite**

```bash
.venv/bin/python -m pytest home/tests.py -v
.venv/bin/python manage.py check
```

Expected: all tests pass, system check reports no issues.

- [ ] **Step 2: curl every page in scope and confirm 200s**

```bash
for path in "/" "/about/" "/inventory/" "/add-host/" "/profile/uitest01.example.com" "/firewall/" "/fwrule/1" "/add-firewall/" "/inventory/upload/" "/firewall/upload/"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:8765${path}")
  echo "GET ${path} -> ${code}"
done
```

Expected: every route returns `200`.

- [ ] **Step 3: Browser-based visual and interaction check**

Using the Chrome browser automation tools (`mcp__claude-in-chrome__*`), open `http://127.0.0.1:8765/` and:
- Confirm the sidebar renders with slate background, blue active-link highlight on the current section, and the top bar shows the page title.
- Navigate to `/inventory/` and `/firewall/` and confirm the context-aware search box appears only on those two pages.
- Click "Create firewall rule" on `/firewall/`, confirm the Bootstrap 5 modal opens (via `bootstrap5.modal.forms.js`, no jQuery), fill and submit the form, confirm it creates a row and the modal closes.
- Open `/add-host/`, confirm the stacked label/input form layout.
- Open `/inventory/upload/`, choose a file, click Upload, confirm the file input was actually inside the form this time (compare against the pre-fix behavior, which silently submitted nothing).
- Check the browser console (`read_console_messages`) on each page for JS errors — expect none, and specifically confirm no `jQuery is not defined` or similar errors.

- [ ] **Step 4: Stop the dev server**

```bash
lsof -ti :8765 | xargs -r kill
```

- [ ] **Step 5: Final commit (only if Step 3 required fixes)**

If the browser check in Step 3 surfaces any visual bugs, fix them in the relevant template from Tasks 6–15 and commit:

```bash
git add -A
git commit -m "Fix issues found during manual browser smoke test"
```

If no fixes were needed, this task ends at Step 4 — no empty commit.
