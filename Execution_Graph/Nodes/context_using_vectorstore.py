
def ContextUsingVectorStore(state):
    retriever=state['key']['retriever']
    question=state['key']['transformed_query']
    retrieved_docs=retriever.invoke(question)
    retrieved_docs=[d.page_content for d in retrieved_docs]
    retrieved_docs="\n\n".join(retrieved_docs)
    state['key']['retrieved_docs']=retrieved_docs
    print("Context retrieved from vectorstore")
    return state