### 🧠 Angel One RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot built using Django and LangChain. It can answer customer support queries based on Angel One's support site and provided insurance documents (`.pdf`, `.docx`). If a query is out of scope, it responds with `"I don't know"`. It has been deployed at https://rag-chatbot-1-1w4e.onrender.com


![Chat UI Screenshot](chat_ui.png)
---

## 🚀 Features

- RAG-based QA using OpenAI and LangChain
- Sources: Angel One Support Website + Insurance PDFs/DOCX
- Returns `"I don't know"` if question is not answerable
- Beautiful chat UI using TailwindCSS
- Stores full conversation history in localstorage so will work even after tab closure and across multiple tabs
- Has clear chat button in case one wants to start from beginning
- Makes use of older conversations to answer like a human
- Has an option to toggle only storing history of last 100 messages for better performance in case of really long conversations

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Unmesh-Kumar/rag_chatbot.git
```

### 2. Set up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Set Environment Variables

Create a .env file in the root with your OpenAI key:

```bash
OPENAI_API_KEY=your_openai_key_here
```


### 4. Set Environment Variables

Create an .env file in the root with your OpenAI key:

```bash
OPENAI_API_KEY=your_openai_key_here
```
This is used in rag_qa.py and vectorstore creation.

### 5. Add the Insurance PDFs

place the insurance pdfs inside chatbot/data/insurance_docs directory

### 6. Index all sources
In the repo the vectordatabase is already provided so this step can be skipped also

To run it for first time and add extra info use this command.
```bash
python manage.py index_sources
```

and if done earlier and want to delete the vector database and make fresh source run this
```bash
python manage.py index_sources --refresh
```

### 7. Run the Server

```bash
python manage.py runserver
```