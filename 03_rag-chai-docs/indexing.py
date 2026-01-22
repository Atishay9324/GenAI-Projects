from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()



#loading the url
loader = RecursiveUrlLoader( "https://docs.chaicode.com/",)
docs = loader.load()


#chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)
split_docs = text_splitter.split_documents(documents=docs)

# vector embedding
embedding_model =OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#using [embedding_model] create embeddings of [split_docs] and store in vector db
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of documents done...")