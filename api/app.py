import os
from flask import Flask, jsonify, request
import pymongo

os.environ['CUDA_VISIBLE_DEVICES'] = "0"
app = Flask(__name__, static_folder='static',)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bigdata"]
chotot_lite = mydb["chotot_lite"]


@app.route('/api/v1.0/houses/', methods=['GET'])
def get_mongo():
    
    dist = request.args.get('dist')
    print(dist)

    myquery = { "area_name": dist }
    query_cursor = chotot_lite.find(myquery, {'_id': False})
    
    return list(query_cursor)

# @app.route('',methods = ['GET'])
# def get_page(page_id):

#     db = connection.test_database          
#     pages = db.pages
#     page = pages.find_one({"id": int(page_id)})  
#     if page == None: 
#         abort(404)
#     return jsonify( { 'page' : make_public_page(page[0])} ) <- error says its not json


if __name__ == '__main__':
    
    app.run(debug = False)
