# AI CSV SQL Agent

An AI-powered CSV SQL Agent built using Python, Streamlit, SQLite, Ollama, and LangChain.

## Features

- Upload CSV files dynamically
- Convert natural language into SQL queries
- Execute SQL queries automatically
- Count missing values
- Find highest/lowest rows
- Download query results
- Interactive data visualization

## Technologies Used

- Python
- Streamlit
- Pandas
- SQLite
- SQLAlchemy
- Ollama
- LangChain

## Installation

### Install Libraries

```bash
pip install -r requirements.txt
```

### Run Ollama

```bash
ollama run llama3
```

### Run Streamlit App

```bash
streamlit run app.py
```

## Example Questions

- Count total rows
- Show highest price row
- Count missing values column wise
- Show average salary
- Show minimum age row

## Project Workflow

CSV Upload → SQLite Database → LLM → SQL Query → Result Display