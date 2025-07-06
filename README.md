# 🧠 Document-based Q&A System using FastAPI + LangChain + FAISS

This project is an AI-powered question answering API that indexes text and PDF documents, performs semantic search using vector embeddings (FAISS), and generates answers using LLMs via Hugging Face Inference API. A Gradio UI is included for interactive usage.

---

## 🚀 Features

- 📄 Upload and index plain text or PDF documents
- 🔍 Semantic search using vector embeddings (FAISS)
- 💬 Question answering using LLMs (e.g., Mistral-7B)
- 🗂️ List and delete indexed documents
- 🖥️ Web UI with [Gradio](https://gradio.app/)
- 📦 Modular architecture: FastAPI + LangChain

---

## 📁 Project Structure

```

.
├── app/
│   ├── api/                # FastAPI routers
│   ├── models/             # Pydantic models
│   ├── services/           # Embedding, LLM, and vector logic
│   ├── utils/              # Text chunking and parsing
│   └── main.py             # FastAPI app entrypoint
    ├── ui.py                   # Gradio UI
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── .gitignore              # Ignore vector DB and envs

````

---

## ⚙️ Tech Stack

| Component       | Tech                          |
|----------------|-------------------------------|
| Language        | Python 3.10+                   |
| API Framework   | FastAPI                        |
| Embeddings      | HuggingFace / LangChain        |
| Vector Store    | FAISS                          |
| LLM Inference   | HuggingFace Inference API      |
| UI              | Gradio                         |

---

## 🛠️ Setup Instructions

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/meetrafay/doc-qa-api.git
cd doc-qa-api
````

### ✅ 2. Create Virtual Env & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🔐 Hugging Face API Key Required

To use embeddings and language model responses via the Hugging Face Inference API, you **must have your own API key**.

### ✅ Get Your Hugging Face API Key

1. Sign up or log in to [HuggingFace.co](https://huggingface.co/join)
2. Go to [Access Tokens](https://huggingface.co/settings/tokens)
3. Click **"New Token"**, choose `read` access
4. Copy the token

### ✅ Set the API Key in Your Local Environment

```bash
export HF_TOKEN=your_token_here     # for Mac/Linux

# or on Windows PowerShell:
$env:HF_TOKEN="your_token_here"



## 🚀 Run the Application

### ✅ Start the FastAPI Backend

```bash
uvicorn app.main:app --reload
```

* API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### ✅ Launch Gradio UI

```bash
python ui.py
```

* UI opens at: [http://localhost:7860](http://localhost:7860)

---

## 🧪 API Endpoints

| Method   | Endpoint               | Description                     |
| -------- | ---------------------- | ------------------------------- |
| `POST`   | `/documents`           | Upload raw text/title JSON docs |
| `POST`   | `/documents/pdf-batch` | Upload multiple PDF files       |
| `GET`    | `/documents`           | List all indexed documents      |
| `POST`   | `/query`               | Ask a question                  |
| `DELETE` | `/documents/{doc_id}`  | Delete a document by ID         |

---

## 💻 Gradio UI Tabs

* Upload text documents
* Upload PDFs
* Ask a question
* List all documents
* Delete by `doc_id`
