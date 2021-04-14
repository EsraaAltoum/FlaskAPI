from flask import Flask, jsonify, request
import requests 
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)


#response message from ping
PING_RESPONSE = {"success": "true"}
TAG_ERROR_RESPONSE = {"error": "Tags parameter is required"}
SORT_BY_ERROR_RESPONSE = {"error": "sortBy parameter is invalid"}
DIRECTION_ERROR_RESPONSE = {"error": "direction parameter is invalid"}


SORT_BY_ACCEPTABLE_VALS = ['id', 'reads', 'likes', 'popularity']
DIRECTION_ACCEPTABLE_VALS = ['asc', 'desc']

#home page of submission
@app.route('/')
def hello_world():
    return 'Welcome to Esraa\'s Submission' 

#ping route
@app.route('/api/ping', methods = ['GET'])
def ping():
    return jsonify(PING_RESPONSE)

#posts route
@app.route('/api/posts', methods = ['GET'])
def posts():
    query_params = request.args 
    tags = query_params.get('tags')
    sort_by = query_params.get('sortBy')
    direction = query_params.get('direction')

    if sort_by and sort_by not in SORT_BY_ACCEPTABLE_VALS:
        return jsonify(SORT_BY_ERROR_RESPONSE), 400
    
    if direction and direction not in DIRECTION_ACCEPTABLE_VALS:
        return jsonify(DIRECTION_ERROR_RESPONSE), 400

    if tags:
        tags_list = tags.split(",")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.ensure_future(get_posts(tags_list))
        loop.run_until_complete(future)
        is_reversed = direction == "desc"
        sort_key = sort_by if sort_by else "id"
        print(future.result().values())
        res = sorted(future.result().values(), key=lambda k: k[sort_key] , reverse=is_reversed)
    else:
        return jsonify(TAG_ERROR_RESPONSE), 400
    
    return jsonify({"posts": res})


async def get_posts(tags):
    results = {}
    with ThreadPoolExecutor(max_workers=10) as executor:
            with requests.Session() as session:
                loop = asyncio.get_event_loop()
                tasks = [loop.run_in_executor(executor, get_post, *(tag, session)) for tag in tags]
                for response in await asyncio.gather(*tasks):
                    for item in response:
                        results[item["id"]] = item 
    return results

def get_post(tag, session):
    url = 'https://api.hatchways.io/assessment/blog/posts?tag=' + tag
    with session.get(url) as response:
        data = response.json().get("posts")
        if response.status_code != 200:
            print("Error: " + url)
        return data
    





