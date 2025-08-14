# 🔐 Cybersecurity Threat Intelligence RAG (Retrieval-Augmented Generation)

This project is an interactive **Streamlit web application** that uses **LlamaIndex** + **ChromaDB** + **Groq LLM** to fetch, process, and query **real-world cybersecurity threat intelligence** from trusted sources like **CISA**, **NVD**, and security vendor advisories.

## 🚀 Features
- Fetches live data from trusted cybersecurity URLs.
- Splits content into embeddings and stores in a **local persistent Chroma vector store**.
- Lets you ask natural language questions about vulnerabilities, CVEs, and threats.
- Returns concise answers **with clickable sources**.
- Fully open-source and runs locally.

## 🏗️ Architecture
![Architecture Diagram](assets/architecture_diagram.png)

1. **User Inputs** — Number of URLs, URLs, and a natural language question in the Streamlit UI.
2. **Web Scraper** — Fetches HTML and converts to clean text.
3. **Chunking & Embedding** — Splits text into chunks and generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
4. **Vector Store (Chroma)** — Stores embeddings persistently on disk for fast similarity search.
5. **Retriever + LLM (Groq)** — Retrieves relevant chunks and generates a concise answer.
6. **Streamlit Output** — Displays the answer and clickable sources.

## 📦 Installation

```bash
git clone https://github.com/<your-username>/cybersecurity-threat-rag.git
cd cybersecurity-threat-rag
pip install -r requirements.txt
```

## 🔑 Environment Variables
```env
GROQ_API_KEY=your_groq_api_key_here
```

## ▶️ Run the App
```bash
streamlit run main.py
```

## 🛠️ Requirements
- Python 3.9+
- Streamlit
- LlamaIndex
- ChromaDB
- Groq API Key

```mermaid
flowchart TB
    %% ==== USER INTERFACE LAYER ====
    subgraph UI["🖥️ User Interface Layer"]
        A[User in Streamlit Web App]
    end

    %% ==== DATA INGESTION LAYER ====
    subgraph Ingestion["🌐 Data Ingestion Layer"]
        B1[URL Loader<br/>(SimpleWebPageReader)]
        B2[HTML to Clean Text Conversion]
        B3[Text Chunking<br/>(SimpleNodeParser)]
    end

    %% ==== EMBEDDING & STORAGE LAYER ====
    subgraph Embedding["🧠 Embedding & Vector Storage Layer"]
        C1[Embedding Generator<br/>(HuggingFace all-MiniLM-L6-v2)]
        C2[Persistent Vector Store<br/>(ChromaDB)]
    end

    %% ==== RETRIEVAL & GENERATION LAYER ====
    subgraph Retrieval["🤖 Retrieval & LLM Layer"]
        D1[Retriever<br/>(Similarity Search)]
        D2[Groq LLM<br/>(Llama 3.3 70B Versatile)]
        D3[Answer Synthesis with Citations]
    end

    %% ==== OUTPUT LAYER ====
    subgraph Output["📄 Output Layer"]
        E1[Answer Displayed in Streamlit]
        E2[Sources as Clickable Links]
    end

    %% ==== FLOW CONNECTIONS ====
    %% User Input to Ingestion
    A -->|Enter URLs & Question| B1
    B1 --> B2 --> B3

    %% Ingestion to Embedding
    B3 --> C1 --> C2

    %% Retrieval Path
    A -->|Query Request| D1
    C2 --> D1 --> D2 --> D3

    %% Final Output
    D3 --> E1
    D3 --> E2

```

## 📚 Example Trusted Sources
- https://www.cisa.gov/news-events/cybersecurity-advisories
- https://nvd.nist.gov/vuln/full-listing
- https://unit42.paloaltonetworks.com/
- https://www.crowdstrike.com/blog/category/threat-intel/
