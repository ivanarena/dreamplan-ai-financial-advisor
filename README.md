# Dreamplan AI Financial Advisor

## Requirements

- Python >=3.9
- uv

## Installation

To install the required packages run the following command:

```bash
uv install
```

Then set up a virtual environment (optional):

```bash
uv venv
```

and activate it:

```bash
source .venv/bin/activate
```

## Usage

To run the app you need to have access to Dreamplan's Calculation API and OpenAI API (stored as environmental variables in a `.env` file in the root of the project, respectively `CALCULATION_API_URL` and `OPENAI_API_KEY`).

If you don't have access to these services you can contact me for trying out the deployed version.

If you wish to run the scraper again (this might replace the current documents used for Retrieval-Augmented Generation) use:

```bash
uv run scraping/scraper.py
```

To run the app use:

```bash
uv run uvicorn main:app --reload
```

## Testing

To run the tests use:

```bash
uv run pytest tests/ -vv
```

To include code coverage:

```bash
uv run pytest tests/ -vv --cov=.
```

## Docker

To build and run the project using docker run:

```bash
docker compose up
```

## Project Structure

The repository is organized as follows:

- `calculation/`: Contains modules for interacting with the calculation API, including client logic, factories, and templates.
- `components/`: Core components for chat, prompt management, retrieval-augmented generation (RAG), and tool integration.
- `db.py`: Database interface and related logic.
- `docker-compose.yml`, `Dockerfile`: Configuration files for containerization and deployment.
- `documents/`: Sample documents in HTML, JSON, and TXT formats for testing and development.
- `experiment/`: Notebooks and scripts for evaluation and experimentation.
- `main.py`: Entry point for running the application.
- `notebooks/`: Jupyter notebooks for product analysis and workflow demonstrations.
- `scraping/`: Web scraping utilities and blacklist management.
- `static/`: Static assets such as images, CSS, and JavaScript files.
- `templates/`: HTML templates for the web interface.
- `tests/`: Unit and integration tests for various modules.
- `pyproject.toml`, `uv.lock`: Project dependencies and environment configuration.

This structure supports modular development, testing, and deployment of the Dreamplan AI Financial Advisor.
