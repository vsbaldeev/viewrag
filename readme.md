# 🎬 ViewRAG: Movie & TV Show Review Analysis System

**AI-powered system that answers questions about media based on real user reviews from TMDB**

## Limitations
- **Language**: english-only support
- **No spoiler protection**: users might know some details about a plot
- **Small database**: review about 40 movies and tv shows

## 🌟 Key Features
- **Hybrid search**: Media title extraction via LLM + metadata filtering in Pinecone
- **Observability**: Call tracing and token tracking via LangSmith
- **Managed services**: Usage of cloud services instead of local solutions


## 🛠️ Technology Stack
| Component | Technology                                    | Why                                                     |
|-----------|-----------------------------------------------|---------------------------------------------------------|
| **LLM** | Groq + Llama 3.1 8B                           | Fast inference, free tier, high limit of tokens per day |
| **Vector DB** | Pinecone (serverless)                         | Managed, scalable, no ops overhead, integrated llama-text-embed-v2 model         | |
| **Observability** | LangSmith                                     | End-to-end tracing and debugging                        |
| **Frontend** | Streamlit                                     | Rapid prototyping and demo                              |


## 🚀 Try It Live
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://viewrag.streamlit.app)

