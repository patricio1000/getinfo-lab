# Get Info Lab

CSC 413 Application Development I: a Django Request Info form. The app
validates the email and phone number, saves valid requests, and redirects
to a thank-you page. Django admin lists the saved requests.

## Run locally (macOS or Linux)

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the form and
http://127.0.0.1:8000/admin/ for admin.

Try `555-1234` to see a validation error, then try `(402) 555-1234`.
The valid request leads to the Thank You page and is stored as
`402-555-1234`. Use fake data for the demo. The settings are for a local
lab, not for production deployment.
