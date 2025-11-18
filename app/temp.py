# from scrape import crawl_dynamic_site
from embed_data import save_to_vector_db
from qa_bot import create_qa_bot
import json
# 1. Crawl website
# scraped_data = crawl_dynamic_site("https://www.yourcollege.ac.in")

# already scraped data 
with open("scraped_data.json", "r", encoding="utf-8") as f:
    scraped_data = json.load(f)

# 2. Store + Embed
vectordb = save_to_vector_db(scraped_data)

# 3. Create QA Chatbot
qa_bot = create_qa_bot(vectordb)

# 4. Ask questions

while(True):
    question = input("Enter question: ")
    response = qa_bot(question)

    print("\nAnswer:")
    print(response["answer"])

# print("\nSources:")
# for doc in answer["source_documents"]:
#     print(doc.metadata["url"])
