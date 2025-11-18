from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def save_to_vector_db(scraped_data):
    texts = [item["text"] for item in scraped_data  ]    
    metadatas = [{"url": item["url"]} for item in scraped_data ]

    embeddings = OpenAIEmbeddings()

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name="college_data"
    )

    return vectordb

# vectordb = save_to_vector_db(data)
# print(vectordb)
