from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

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


def get_answer(query):
   # Load vector store
   vectorstore = FAISS.load_local(VECTORSTORE_PATH, OpenAIEmbeddings())
   retriever = vectorstore.as_retriever(search_kwargs={SEARCH_KWARGS_K: SEARCH_KWARGS})

   # Create chain with custom prompt and fallback
   def validate_response(response):
      cleaned = response.strip().lower()
      if cleaned in NOT_KNOWN_WORDS or len(cleaned) < 10:
         return RESPONSE_TO_RETURNED
      return response

   rag_chain = (
      {CONTEXT_KEY: retriever, QUESTION_KEY: RunnableLambda(lambda x: x[QUESTION_KEY])}
      | RAG_PROMPT
      | ChatOpenAI(model=MODEL_TO_BE_USED)
      | StrOutputParser()
      | RunnableLambda(validate_response)
   )

   # Run the chain
   result_text = rag_chain.invoke({QUESTION_KEY: query})
   sources = [doc.metadata[SOURCE_KEY] for doc in retriever.get_relevant_documents(query)]
   return result_text, sources