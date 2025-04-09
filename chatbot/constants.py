# Paths
INSURANCE_DOC_DIR = "data/insurance_docs"
VECTORSTORE_PATH = "vectorstore/insurance_all"

# Site constangts
SUPPORT_SITE_URL = "https://www.angelone.in/support"
SUPPORT = "support"

# Extensions
PDF_EXTENSION = ".pdf"
DOCX_EXTENSION = ".docx"

# Chars
NEWLINE = "\n"

# Keys
TEXT_KEY = "text"
METADATA_KEY = "metadata"
SOURCE_KEY = "source"
TYPE_KEY = "type"
RESULT_KEY = "result"
CONTEXT_KEY = "context"
QUESTION_KEY = "question"
ANSWER_KEY = "answer"
ERROR_KEY = "error"
SOURCE_DOCUMENTS_KEY = "source_documents"
SEARCH_KWARGS_K = "k"

#Parser
HTML_PARSER = "html.parser"


# Tags
P_TAG = "p"
LI_TAG = "li"
H1_TAG = "h1"
H2_TAG = "h2"
H3_TAG = "h3"
A_TAG = "a"
HREF_TAG = "href"

# Configs
SITE_REQUEST_RETRIES = 3
SITE_REQUEST_TIMEOUT = 20
SITE_REQUEST_BACKOFF = 5

# Source
FILE_SOURCE = "file"
WEB_SOURCE = "web"

# Chunk Config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# command line flags
REFRESH_FLAG = "--refresh"

# LLM RAG config
SEARCH_KWARGS = 3
MODEL_TO_BE_USED = "gpt-3.5-turbo"


# Response Logic
NOT_KNOWN_WORDS = ["", "i don't know", "idk", "not sure"]
RESPONSE_TO_RETURNED = "I Don't know"


# Prompt Template
PROMPT_TEMPLATE = """You are a very firendly and helpful assistant which communicates like a human and answers questions only using the provided context.
If the answer is not in the context, respond with "I don't know". Below I can have greetings and other communication also in place of question do not reply I don't know if there is no specific question but give human like response

Context:
{context}

Question:
{question}

Answer:"""