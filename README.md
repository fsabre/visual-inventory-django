# Visual-Inventory

Collaboratively organize your physical storage location and easily find the places to store a thing, or the places to
fetch this thing.

You can fill your global physical storage with several sublocations, that will contain their own sublocations, etc.

## Run Locally

Start by cloning the project.

```bash
git clone https://github.com/fsabre/visual-inventory-django.git
cd visual-inventory-django/
```

Install the backend.

```bash
python -m venv venv  # Maybe python3 depending on your system
source venv/bin/activate
pip install -r requirements.txt
cd src/
python manage.py migrate
python manage.py createsuperuser
```

Install the frontend.

```bash
cd frontend/
npm install
```

Then, when you want to run the backend :

```bash
source venv/bin/activate
cd src/
python manage.py runserver localhost:8000
```

The admin dashboard will be available at http://localhost:8000/admin.

And to run the frontend :

```bash
cd frontend/
npm run dev
```

The user app will be available at http://localhost:5173/.

## TODO

### Features

- Add an editable state for locations (to tidy, to label, done)

### Fix

- The parent of a Location can't be self or children.
- Optimize queries

### Deployment

- Include the project in a Docker image
