import os
import re
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
load_dotenv()

def VectorStoreCreator(urls,num_results=2,vectorstore_dir_path="VectorStore"):
    print("Creating Retriever")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001",
                                                   api_key=os.environ['GOOGLE_GEMINI_API_KEY'])
    if os.path.exists(vectorstore_dir_path):
        print("Using Created Vectorstore")
        # vectorstore=Chroma(
        #     persist_directory=vectorstore_dir_path,
        #     embedding_function=embedding_model
        # )

    else:
        print("Creating Vectorstore")
        os.makedirs(vectorstore_dir_path,exist_ok=True)
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]
        doc_data=[re.sub(r'\s\s+', ' ', d.page_content) for d in docs_list]


        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=750,
            chunk_overlap=75
        )

        split_text=[text_splitter.split_text(text) for text in doc_data]
        text=[t for inst in split_text for t in inst]

        vectorstore=Chroma(
            embedding_function=embedding_model,
            persist_directory=vectorstore_dir_path
        )
        vectorstore.add_texts(text)
        vectorstore.persist()


    # return vectorstore_dir_path
    # retriever = vectorstore.as_retriever(search_type="mmr",search_kwargs={"k":num_results})
    # print("Retriever Created..")
    return vectorstore_dir_path







