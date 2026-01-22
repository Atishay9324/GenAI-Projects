from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI

load_dotenv()

client = OpenAI()

# vector embedding
embedding_model =OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#making connections with the db
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

#take user query
query = input("> ")

#vector similarity search [query] in db

search_result = vector_db.similarity_search(
    query=query
)

for result in search_result:
    print(result.page_content)

# context = "\n\n\n".join([f"Page Content: {result.page_content}\nURL: {result.metadata['source']}" for result in search_result])

# SYSTEM_PROMPT = f"""
#     You are a helpfull AI Assistant who asnweres user query based on the available context
#     retrieved from a Website along with page_contents and URL.

#     You should only answer the user based on the following context and navigate the user
#     to open the right page number to know more.

#     Context:
#     {context}
# """

# chat_completion= client.chat.completions.create(
#     model="gpt-4.1-mini",
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": query},
#     ]
# )

# print(f"🤖: {chat_completion.choices[0].message.content}")