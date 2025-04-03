# Welcome to the documentation

## Installation guide

Prerequisites: Python 3.12.3, MySQL server setup

1. Clone the repository

```
git clone <repository-url>
cd <repository-directory>
```

2. Make a virtual environment folder (named .venv or whatever preferred) and activate it using commands

For mac/linux:

```
python3 -m venv .venv
source .venv/bin/activate
```

For windows:

```
python -m venv .venv
.venv\Scripts\activate
```

2. Install Dependencies with pip:
   ```pip install -r requirements.txt```

3. Run your application

```
uvicorn main:app --reload
```

