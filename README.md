### Requirement for server:
    libmagic:
        linux:
            sudo apt install libmagic1 python3-magic
        maxOs:
            brew install libmagic

### Set Development Environment

    set -o allexport;source ./env/dev.env; set +o allexport

### Collect schema
    python manage.py spectacular --file schema.yml

## Local Setup

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate virtual environment: `source .venv/bin/activate`
4. Install requirements: `pip install -r requirements/local.txt`
5. Copy .env.example to .env and update values
6. Run migrations: `python manage.py migrate`
7. Setup project: `python manage.py setup_project`

