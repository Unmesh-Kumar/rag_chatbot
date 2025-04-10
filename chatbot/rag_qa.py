from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI

from langchain.prompts import PromptTemplate

from .constants import (
   VECTORSTORE_PATH,
   SEARCH_KWARGS,
   SOURCE_KEY,
   SOURCE_DOCUMENTS_KEY,
   SEARCH_KWARGS_K,
   MODEL_TO_BE_USED,
   RESULT_KEY,
   NOT_KNOWN_WORDS,
   RESPONSE_TO_RETURNED,
   PROMPT_TEMPLATE,
   CONTEXT_KEY,
   QUESTION_KEY
)

# Prompt with fallback instruction
RAG_PROMPT = PromptTemplate.from_template(PROMPT_TEMPLATE)

# Caution: I am using allow_dangerous_deserialization=True as I trust this vectorDatabase
vectorstore = FAISS.load_local(
   VECTORSTORE_PATH,
   OpenAIEmbeddings(),
   allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={SEARCH_KWARGS_K: SEARCH_KWARGS})


def get_answer_with_history(query, history):
   global vectorstore
   global retriever
   context_docs = retriever.get_relevant_documents(query)
   context = "\n\n".join(doc.page_content for doc in context_docs)

   # Combining history into a single string
   formatted_history = "\n".join(
      f"{item['role'].capitalize()}: {item['content']}" for item in history
   )

   prompt_input = PROMPT_TEMPLATE.format(
      context=context,
      question=query,
      history=formatted_history
   )

   llm = ChatOpenAI(model=MODEL_TO_BE_USED)
   response = llm.invoke(prompt_input).content.strip()

   cleaned = response.lower()
   if cleaned in NOT_KNOWN_WORDS:
      response = RESPONSE_TO_RETURNED

   sources = [doc.metadata[SOURCE_KEY] for doc in context_docs]

   return response, sources