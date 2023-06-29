import streamlit as st
import s3fs
import os
import openai
from dotenv import load_dotenv
from llama_index import load_index_from_storage, StorageContext, Document

def persist_storage(index, s3, s3_bucket):
    # persist storage
    index.storage_context.persist(s3_bucket, fs=s3)

def index_storage(s3, s3_bucket):
    # load index from s3
    storage_context = StorageContext.from_defaults(persist_dir=s3_bucket, fs=s3)
    # return index
    return load_index_from_storage(storage_context, 'vector_index')

def refresh_store(index, documents):
    refresh_doc = index.refresh_ref_docs(documents)

def process_to_documents(docs):
    for uploaded_file in docs:
        document_text = uploaded_file.read()
        st.write("filename:", uploaded_file.name)
        return [Document(text=document_text.decode('utf-8'))]

def handle_userinput(user_question, index):
    query_engine = index.as_query_engine()
    result = query_engine.query(user_question)
    st.write(result.response)

def main():
    load_dotenv()

    AWS_KEY= os.getenv('AWS_KEY', default='MISSING KEY')
    AWS_SECRET= os.getenv('AWS_SECRET', default='MISSING KEY')
    s3_bucket= os.getenv('BUCKET', default='MISSING KEY')

    openai.api_key= os.getenv('OPENAI_API_KEY', default='MISSING KEY')

    # setup S3 file system
    s3 = s3fs.S3FileSystem(
        key=AWS_KEY,
        secret=AWS_SECRET,
        config_kwargs={'region_name': 'us-west-2'},
        s3_additional_kwargs={'ACL': 'public-read-write'}
    )

    # set page title
    st.set_page_config(page_title="Llamaindex + S3 index storage", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

    st.header("What would you like to know?")

    # capture user query
    user_question = st.text_input("Ask a question about your documents:")

    # get storage index from s3
    index = index_storage(s3, s3_bucket)
    
    if user_question:
        handle_userinput(user_question, index)

    with st.sidebar:
        st.subheader("Your documents")
        uploaded_docs = st.file_uploader(
            "Upload your files here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):

                # process the uploaded files and convert to documents
                docs = process_to_documents(uploaded_docs)
            
                # refresh the store with the new documents
                refresh_store(index, docs)

                # persist updated store
                persist_storage(index, s3, s3_bucket)


if __name__ == '__main__':
    main()
