from pymongo import MongoClient
# from langchain_community.embeddings.openai import OpenAIEmbeddings
# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
# from langchain_community.llms import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
# import json
import json

# Assuming your JSON file is named "data.json"
with open('raw.json') as f:
    documents = json.load(f)
# import key_parm

client = MongoClient("mongodb+srv://20z342:cBwPEGWx2iMWCUyE@cluster0.xdefz6l.mongodb.net/")
dbName = "complaints"
collectionName = "user_locations"
collection = client[dbName][collectionName]

# loader = DirectoryLoader('./sample_files',glob="./*.txt",show_progress=True)
# data = loader.load()

# documents = json.
# embeddings = OpenAIEmbeddings(openai_api_key=key_parm.openai_api_key)

# vectorStore = MongoDBAtlasVectorSearch.from_documents( data , embeddings , collection=collection)

  


for document in documents:
    collection.insert_one(document)
