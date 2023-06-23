import streamlit as st
import s3fs
import os
import openai
from dotenv import load_dotenv
from llama_index import load_index_from_storage, StorageContext


def handle_userinput(user_question, index):
    query_engine = index.as_query_engine()
    result = query_engine.query(user_question)
    st.write(result.response)


def main():
    load_dotenv()

    openai.api_key= os.getenv('OPENAI_API_KEY')

    AWS_KEY= os.getenv('AWS_KEY')
    AWS_SECRET= os.getenv('AWS_SECRET')
    BUCKET= os.getenv('BUCKET')
    KEY= os.getenv('BUCKET_STORAGE_KEY')

    # set page title
    st.set_page_config(page_title="Llamaindex + S3 index storage", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

    s3 = s3fs.S3FileSystem(
        key=AWS_KEY,
        secret=AWS_SECRET,
        config_kwargs={'region_name': 'us-west-2'},
        s3_additional_kwargs={'ACL': 'public-read-write'}
    )

    # load index from s3
    persist_dir = f'{BUCKET}/{KEY}'
    sc = StorageContext.from_defaults(persist_dir=persist_dir, fs=s3)

    index = load_index_from_storage(sc, 'vector_index')

    st.header("What would you like to know?")

    user_question = st.text_input("Ask a question about your documents:")
    
    if user_question:
        handle_userinput(user_question, index)

if __name__ == '__main__':
    main()
