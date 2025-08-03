<span style="color:#4caf50;"><b>Created:</b> 2025-08-03</span> | <span style="color:#ff9800;"><b>Updated:</b> 2025-08-03</span> | <span style="color:#2196f3;"><b>Author:</b> Gouse Shaik</span>

This is a **simple local setup** for a RAG-based DevOps assistant using an LLM on your **machine with 8 GB RAM** and **600 GB storage** (CPU-only, no GPU).

---

## ✅ What You’ll Get

A fully working local RAG system to:

- Ask questions about CI/CD, Bash, YAML
    
- Search your own markdown, PDF, scripts
    
- Answer using a **lightweight local LLM**
    

---

## ⚙️ Your Machine Constraints

|Spec|Status|
|---|---|
|8 GB RAM|✅ Fine for 4-bit models (`Q4_K_M`)|
|600 GB Disk|✅ More than enough|
|CPU-only|✅ Will use `llama-cpp-python`|

---

## 🧩 Tools Used

|Component|Tool|
|---|---|
|LLM|`mistral-7b-instruct.Q4_K_M.gguf`|
|Embeddings|`all-MiniLM-L6-v2` (HuggingFace)|
|Vector DB|`Chroma`|
|Language Layer|`LangChain`|
|Inference|`llama-cpp-python`|
|Interface|CLI|

---

## 🛠 Setup Instructions (One-by-One)

### 1. 🧪 Create a clean Python env

```bash
python3 -m venv rag-devops
source rag-devops/bin/activate
```

---

### 2. 📦 Install dependencies

```bash
pip install llama-cpp-python langchain chromadb sentence-transformers pypdf
```

---

### 3. 📁 Create directory structure

```bash
mkdir -p devops-rag/{data,embeddings,model}
cd devops-rag
```

---

### 4. ⬇️ Download GGUF model

Download the model from:  
👉 [https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

Pick:  
🟩 `mistral-7b-instruct-v0.1.Q4_K_M.gguf`

Put it in:

```bash
devops-rag/model/mistral-7b-instruct.Q4_K_M.gguf
```

---

### 5. 🧠 Paste this into `load_and_index.py`

```python
from langchain.document_loaders import TextLoader, PDFMinerLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from sentence_transformers import SentenceTransformer
import os

EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
DATA_DIR = "data"

def load_docs():
    docs = []
    for root, _, files in os.walk(DATA_DIR):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".pdf"):
                docs.extend(PDFMinerLoader(path).load())
            else:
                docs.extend(TextLoader(path).load())
    return docs

def index_documents():
    docs = load_docs()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    texts = [chunk.page_content for chunk in chunks]
    metadatas = [chunk.metadata for chunk in chunks]
    embeddings = EMBEDDING_MODEL.encode(texts).tolist()

    db = Chroma.from_embeddings(texts=texts, embedding=embeddings, metadatas=metadatas, persist_directory="embeddings")
    db.persist()

if __name__ == "__main__":
    index_documents()
```

---

### 6. 🧠 Paste this into `query.py`

```python
from langchain.vectorstores import Chroma
from langchain.llms import LlamaCpp
from sentence_transformers import SentenceTransformer

DB_DIR = "embeddings"
MODEL_PATH = "model/mistral-7b-instruct.Q4_K_M.gguf"
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def get_relevant_chunks(query, k=4):
    vectordb = Chroma(persist_directory=DB_DIR)
    embedded = EMBEDDING_MODEL.encode([query]).tolist()[0]
    return vectordb.similarity_search_by_vector(embedded, k=k)

def ask_llm(context, question):
    context_text = "\n".join([doc.page_content for doc in context])
    prompt = f"""### Instruction:
You are a DevOps assistant. Based on the context below, answer the question.

### Context:
{context_text}

### Question:
{question}

### Answer:"""

    llm = LlamaCpp(
        model_path=MODEL_PATH,
        n_ctx=2048,
        temperature=0.3,
        max_tokens=512,
        n_threads=4,
        verbose=False
    )
    return llm(prompt)

if __name__ == "__main__":
    while True:
        q = input("\nAsk your DevOps assistant: ")
        if q.lower() == "exit": break
        docs = get_relevant_chunks(q)
        answer = ask_llm(docs, q)
        print("\n🔧 Answer:\n", answer)
```

---

### 7. 🚀 Add files to `data/` folder

Put your `.md`, `.sh`, `Jenkinsfile`, `.yaml`, `.pdf` in `devops-rag/data/`

---

### 8. 🧠 Build the vector DB

```bash
python load_and_index.py
```

---

### 9. 🤖 Ask questions!

```bash
python query.py
```

Then ask:

```text
How does this Jenkinsfile deploy to staging?
What does this bash script do in step 3?
Explain how to rollback a Helm chart using this doc
```

---

## 🧩 Optional Add-ons

|Need|Suggestion|
|---|---|
|Web UI|Add `streamlit` interface|
|Dockerized|Wrap in container + mount volumes|
|PDF OCR|Use `unstructured` + Tesseract|

---

Let me know if you want:

- A `streamlit` version of this
    
- Docker setup
    
- Autoloader that watches a Git repo
    

I’ll give that in one shot too.