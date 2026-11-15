# Study Hub

A local Django learning project alongside the original Orbital website.
The existing `dist/solar-system.html`, planet images, CSS and JavaScript are preserved.

## Run on Windows (PowerShell)

```powershell
cd C:\Users\gordo\solar_system\orbital
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Open http://127.0.0.1:8000/ for Study Hub, then click Science.
Science Study is at http://127.0.0.1:8000/science/.
Keep the terminal running. Press Ctrl+C to stop the server; run `deactivate`
to leave the virtual environment.

If PowerShell blocks activation, run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`, then retry.
You can also skip activation and use
`.\.venv\Scripts\python.exe manage.py runserver`.

For a new environment, install `requirements.txt` and run
`python manage.py migrate` before starting the server. A migration creates or
updates database tables. The local `db.sqlite3` file is ignored by Git.

## How a page works

1. `config/` is the Django **project**: settings for the whole site.
2. `learning/` is an **app**: a group of related features.
3. `config/urls.py` passes page addresses to `learning/urls.py`.
4. `learning/urls.py` matches an address to a **view**, a Python function.
5. `learning/views.py` renders a **template**, an HTML file, for that page.
6. Templates in `learning/templates/learning/` share `base.html` for their layout.
7. **Static files** are CSS, JavaScript and images. New styling lives in
   `learning/static/learning/study.css`.

The Science link uses a named URL (`learning:science`) so Django builds the
address. To add Math or English, add a view in `views.py`, a named route in
`learning/urls.py`, and a template extending `learning/base.html`. Replace the
subject's Coming soon text in `home.html` with a link using that route name.

## Original explorer

During local development, Django serves the untouched `dist/` folder under
`/static/explorer/`, keeping the original relative image and page links working.
The Science page links to `/static/explorer/solar-system.html`; the original
gallery is `/static/explorer/index.html`.

This setup runs locally with Django's development server. The existing static
hosting configuration does not run this Python application.

## Student accounts

- `/accounts/signup/` uses Django's `UserCreationForm` to validate usernames,
  confirm passwords, apply the configured password rules, and store password
  hashes. The signup view signs the new student in and redirects home.
- `/accounts/login/` uses Django's `LoginView` and its authentication form.
  `/accounts/logout/` uses `LogoutView`, submitted through a CSRF-protected
  POST button in the shared header. Both redirect home by default, as configured
  in `config/settings.py`.
- `login.html` and `signup.html` extend the shared layout and display Django's
  validation errors and help text. `study.css` styles the account forms.
- `home.html` displays the authenticated student's username using the existing
  authentication template context processor. Django escapes the username.
  Visitors can continue to browse the public home and science pages.

Run migrations and local checks with the project's virtual environment:

```powershell
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

For a manual check, start the server, open `/accounts/signup/`, and create an
account. Confirm your username appears on the home page, log out, then log in
again. Try an incorrect password and a duplicate username to see form errors.
Automated tests cover these flows, password hashing and validation, CSRF
protection, POST-only logout, and rejection of external login redirects.
