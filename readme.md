# 🎬 ViewRAG: Movie & TV Show Review Analysis System

## 🛠️ Technical Stack

- **Data Collection**: TMDb API with Python `requests`
- **Vector Database**: ChromaDB with persistent storage
- **Embeddings**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **LLM Inference**: Ollama with Llama 3.2 3B model
- **Frontend**: Streamlit
- **Environment Management**: Python `dotenv`

## 🚀 Quick Start

### Prerequisites
- Python 3.13
- Ollama installed and running ([Download Ollama](https://ollama.com/))
- TMDb API key (register at [themoviedb.org](https://www.themoviedb.org/settings/api))

### Installation
```bash
python3.13 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Running project

```bash
touch .env # TMDB_API_KEY=<your token>
mkdir data
python3.13 fetch_tv_datasets.py
python3.13 fetch_reviews.py
python3.13 create_embeddings.py
streamlit run app.py
```
