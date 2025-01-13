import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from google.oauth2 import service_account
load_dotenv()

# with open("gen-lang-client-0757914490-a870ef8fa203.json","r") as file:
#     json_account_info=json.load(file)

credentials = service_account.Credentials.from_service_account_file("gen-lang-client-0630959595-717d9b7bf4b2.json")

def ContextUsingVectorStore(state):

    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                   api_key=os.environ['GOOGLE_GEMINI_API_KEY'],
                                                   credentials=credentials)
    vectorstore=Chroma(
        persist_directory=state["key"]["vectorstore_path"],
        embedding_function=embedding_model

    )
    retriever=vectorstore.as_retriever(search_type="mmr", search_kwargs={"k":3})
    question=state['key']['transformed_query']
    retrieved_docs=retriever.invoke(question)
    retrieved_docs=[d.page_content for d in retrieved_docs]
    retrieved_docs="\n\n".join(retrieved_docs)
    state['key']['retrieved_docs']=retrieved_docs
    print("Context retrieved from vectorstore")
    return state