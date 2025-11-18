from langchain_openai import ChatOpenAI

def create_qa_bot(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    def qa_chain(question):
        # 1) Retrieve documents
        docs = retriever.invoke(question)

        # 2) Combine the text manually (this replaces create_stuff_documents_chain)
        context = "\n\n".join([d.page_content for d in docs])

        # 3) Build final prompt (this replaces create_retrieval_chain)
        prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:
        """

        # 4) Call OpenAI
        result = llm.invoke(prompt)

        return {
            "answer": result.content,
            "context": docs
        }

    return qa_chain
