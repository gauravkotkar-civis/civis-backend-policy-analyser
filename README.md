# CIVIS - AI Policy Document Compliance Audit Checker Backend Application

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install uv
make venv
source .venv/bin/activate
make install
export SOURCE_DIR=~/civis-ai-backend/src
```

## Usage

## Setup Project

### Create virtual env using `uv`

```
$ make venv
```

### Run and fix lint errors

```
$ make fix
```

### Install dependences

```
$ make install
```


## Initialize Database migration using Alembic

### Step 1: Initialize alembic inside source directory
```
$ alembic init -t async src/civis_backend_policy_analyser/alembic
```

### Step 2: Create data base tables revisions for the SQLAlechemy models to generate database tables.
```
$ alembic revision --autogenerate -m "<Revision-Message>"
```

### Step 3: Create Database migration or execute Database queries using alembic.
```
$ alembic upgrade head
```

## Run Fast API Application localhost server.

```
export PYTHONPATH=/home/user/civi-backend-policy-analyser/src:$PYTHONPATH
cd src;
python -m civis_backend_policy_analyser.api.app
```

## Test

```
export PYTHONPATH=~/civis-ai-backend/src
make test
make cov
```