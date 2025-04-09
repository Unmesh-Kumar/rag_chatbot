from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings

from .insurance_utils import load_documents
from .website_utils import get_all_support_links, extract_text_from_url

from .constants import VECTORSTORE_PATH, TEXT_KEY, METADATA_KEY, SOURCE_KEY, TYPE_KEY,\
FILE_SOURCE, WEB_SOURCE, CHUNK_SIZE, CHUNK_OVERLAP


def get_all_docs_from_local_insurance_documents():
   all_docs = []
   docs = load_documents()
   for d in docs:
      all_docs.append({
         TEXT_KEY: d[TEXT_KEY],
         METADATA_KEY: {
            SOURCE_KEY: d[METADATA_KEY][SOURCE_KEY],
            TYPE_KEY: FILE_SOURCE
         }
      })
   
   return all_docs


def get_all_docs_from_angelone_support_site():
   all_docs = []
   links = get_all_support_links()
   order = 1
   for link in links:
      print(f"scraping {order} out of {len(links)} total pages")
      text = extract_text_from_url(link)
      if text.strip():
         all_docs.append({
               TEXT_KEY: text,
               METADATA_KEY: {
                  SOURCE_KEY: link,
                  TYPE_KEY: WEB_SOURCE
               }
         })
      order +=1
   
   return all_docs


def get_all_chunks():
   splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
   chunks = []
   for doc in all_docs:
      split_chunks = splitter.create_documents([doc[TEXT_KEY]], metadatas=[doc[METADATA_KEY]])
      chunks.extend(split_chunks)
   return chunks


def save_all_the_chunks_in_vector_database(chunks):
   embeddings = OpenAIEmbeddings()
   vectorstore = FAISS.from_documents(chunks, embeddings)
   vectorstore.save_local(VECTORSTORE_PATH)


def index_all_sources():
   all_docs = []

   print("Loading all local insurance documents...")
   all_docs.extend(get_all_docs_from_local_insurance_documents())

   print("Scraping support pages...")
   all_docs.extend(get_all_docs_from_angelone_support_site())
   
   print(f"Loaded {len(all_docs)} documents.")

   chunks = get_all_chunks()
   print(f"Created {len(chunks)} chunks")

   save_all_the_chunks_in_vector_database(chunks)
   print("Vector store saved.")