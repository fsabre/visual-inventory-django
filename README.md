# Visual-Inventory

Collaboratively organize your physical storage location and easily find the places to store a thing, or the places to
fetch this thing.

You can fill your global physical storage with several sublocations, that will contain their own sublocations, etc.

## Run Locally

Clone the project.

```bash
git clone https://github.com/fsabre/visual-inventory-django.git
cd visual-inventory-django/
```

Install the backend.

```bash
python -m venv venv
source venv\bin\activate
pip install -r requirements.txt
```

Install the frontend.

```bash
cd frontend
npm install
```

Run the backend with :

```bash
source venv\bin\activate
cd src/
python manage.py runserver localhost:8000
```

Run the backend with :

```bash
cd frontend/
npm run dev
```

## TODO

### Features

- Make a search mode that highlights the locations that contain a category
- Add a editable state for locations (to tidy, to label, done)

### Fix

- Rename the app to "visualinventory" and the project to "?"
- The parent of a Location can't be self or children.
- Optimize queries

### Deployment

- Include the project in a Docker image
