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
HISTORY_KEY = "history"
SOURCES_KEY = "sources"
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
PROMPT_TEMPLATE = """
You are a very firendly and helpful assistant which communicates like a human 
and answers questions due to being trained on customer support documentation to 
assist users. The relevant customer support documentation will be provided to you 
below as the context. If the answer is not in the context, respond with "I don't know". 
Like you don't have to answer general knowledge questions. For example on being asked
Who is narendra modi?
Where is dublin? 
when was google started? 
when was world war 2 started? 
which food sources are good protein etc 
you don't have to answer as they are not the questions answerable using the context.
They are not the exhaustive examples. Every question that cannot be answered using the
given context should not be anwsered are not in context and not relevant to your job. 
Below I can have greetings and other communication like thanking etc also in place of 
question do not reply I don't know if there is no specific question but give human 
like response so that you appear friendly. You will also be given the whole history 
of conversation so that you can understand the whole context.

Context:
{context}

Conversation History:
{history}

Question:
{question}

Answer:
"""