from fastapi import FastAPI, Request
import urllib.parse
import json
from location import perform_location_query
from openai import OpenAI
import constants
from classify import dept
import key_parm

from pymongo import MongoClient

# Assuming you have a MongoDB client set up
client = MongoClient(key_parm.MONGO_URI)
db = client['complain']
collection = db['user_complaints']





def toDict(embedded):
    return dict(item.split("=") for item in urllib.parse.unquote(embedded).split("&"))

# Decode the body using urllib.parse.unquote

app = FastAPI()

@app.get("/")
def first_example():
    return {"GFG Example": "FastAPI"}

@app.post("/test")
async def test_post(request: Request):
    raw = await request.body()
    # print(f"POST request body: {raw.decode('utf-8')}")
    body = toDict(raw.decode('utf-8'))
    extracted = perform_location_query(float(body["latitude"]), float(body["longitude"]))
    complaints = extracted["complaints"]
    urls = extracted["urls"]
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": f"{constants.systemPrompt}"},
        {"role": "user", "content": f"{constants.queryPrompt} {complaints}"}
    ]
    )


    
    return {"message": f"{completion.choices[0].message.content}",
            "urls" : urls}


@app.post("/classify")
async def classify_complaint(request: Request):
    raw = await request.body()
    # print(f"POST request body: {raw.decode('utf-8')}")
    body = toDict(raw.decode('utf-8'))

    # ans = dept(body['complaint'].replace('+',' '))
    print(type(body['complaint']))
    temp = body["complaint"]
    print(temp)
    v = temp.replace('+',' ')
    # print(type(v))
    d = dept(v , float(body['latitude']) , float(body['longitude']))
    print(d)
 
    return {"message" : f"{d}"}



@app.post("/register")
async def classify_complaint(request: Request):
    raw = await request.body()
    # print(f"POST request body: {raw.decode('utf-8')}")
    body = toDict(raw.decode('utf-8'))
    body['complaint'].replace('+',' ')
    print(str(body))

    result = collection.insert_one(body)

    # print(result.inserted_id)
    # print(result.inserted_id)
#     inserted_id = result.inserted_id

# # Print the inserted _id
# p   rint(f"Inserted document with _id: {inserted_id}")

    return {"message" : f"{result.inserted_id}"}


