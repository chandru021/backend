
from pymongo import MongoClient
# import requests
import openai
import key_parm
import pandas as pd
from openai import OpenAI


def generate_embedding(text : str) -> list[float]:
   
    EMBEDDING_MODEL = "text-embedding-3-small"
    # count = 9960
    openai.api_key = key_parm.openai_api_key
    embedding = openai.embeddings.create(input=text, model=EMBEDDING_MODEL).data[0].embedding

    return embedding


def dept(query: str , lat : float , lon : float):
    df = pd.read_excel('complaint_counts_updated.xlsx')

    # Create a dictionary from the Excel data
    mapping_dict = dict(zip(df['org_code'], df['full_form']))

    # Print the dictionary
    # print(mapping_dict)


    client = MongoClient(key_parm.MONGO_URI)
    dbName = "complain"
    collectionName = "history"
    collection = client[dbName][collectionName]






    necessary = []
    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": generate_embedding(query),
                "path": "embedding_complaint",
                "numCandidates": 100,
                "limit": 4,
                "index": "default",
            }
        }
    ])

    for document in results:
        temp = {}
        temp['org_code'] = document['org_code']
        temp['subject_content_text'] = document['subject_content_text']
        necessary.append(temp)
    
    client2 = OpenAI()

    completion = client2.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"you are a public grievance officer who classifies which department a complaint should go to , they will always go to one among the following list ONLY , this contains a list of mappings of org_codes, full_forms of the departments {str(mapping_dict)} , previously there were similar similar complaints which were classified , use it as context {necessary}"},
            {"role": "user", "content": f"given the previouse classifications of problems related to the current problem which department should the current problem go to {query}, location of the complaint is 11.3410° N, 77.7172° E, make sure to consider the location also while makeing a SMART decision, reply only the org_code ,"}
        ]
    )

    return completion.choices[0].message.content