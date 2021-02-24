# GCP Workshop

Few artifacts to support a GCP workshop.

## Data

Synthetic data generator.

## Server

Serves predictions from a model that has been trained using GCP's AI platform.

## Running locally

Setting up the environment:

```bash
# Create and activate venv.
python3 -m venv venv
source venv/bin/activate

# Install package and dependencies.
pip install -e .
pip install -r requirements-dev.txt
```

Generating data:

```bash
python -m data.generate_data
```

Run prediction server:

```bash
docker-compose up
```
