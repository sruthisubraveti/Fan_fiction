from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
import os

#test_fan_fic_v313
test_fan_fic_v3 = Flask(__name__)

# Connect to MongoDDB
client = MongoClient("mongodb://localhost:27017/")
db = client["bull_fitting"]
user_collection = db["user"]
story_collection = db["story"]
movie_collection = db["movies"]

@test_fan_fic_v3.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is Ssubmitted, handle the form data as before
        name = request.form.get('name')
        movie = request.form.get('movie')
        story = request.form.get('story')
        current_datetime = datetime.now()
        created_on = int(current_datetime.timestamp())

        story_document = {
            "name": name,
            "movie": movie,
            "story": story,
            "created_on": current_datetime
        }
        user_document = {
            "name": name
        }
        movie_document = {
            "movie": movie
        }

        story_collection.insert_one(story_document)
        user_collection.insert_one(user_document)
        movie_collection.insert_one(movie_document)

        return redirect(url_for('index'))
    else:
        # If the requesSt method is GET, retrieve all data from MongoDB
        data = list(story_collection.find().sort("created_on", -1))

        return render_template('Fan_Fic_main.html', data=data)

@test_fan_fic_v3.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    # Query MongoDB collectTion based on the usSer's search query
    search_data = list(story_collection.find({'movie': {'$regex': query, '$options': 'i'}}).sort("created_on", -1))
    
  # Fetch all data from MongoDB if there are no search results
    if not search_data:
        data = list(story_collection.find().sort("created_on", -1))
        #return render_template('Fan_Fic_mainja.html', data=data)

    return render_template('Fan_Fic_main.html', data=search_data)

@test_fan_fic_v3.route('/refresh', methods=['POST'])
def refresh():
    data = list(story_collection.find().sort("created_on", -1))

    return render_template('Fan_Fic_main.html', data=data)

@test_fan_fic_v3.route('/delete', methods=['POST'])
def delete():
      # Get the IDs of documents to delete
    ids_to_delete = request.form.getlist('document_id')
    
    # Delete the selected documents
    for document_id in ids_to_delete:
        story_collection.delete_one({"_id": ObjectId(document_id)})
    data = list(story_collection.find().sort("created_on", -1))
    return render_template('Fan_Fic_main.html', data=data)

@test_fan_fic_v3.route('/image/<path:filename>')
def download_file(filename):
    return send_from_directory('/Users/tjdamineni/Desktop/Grad_Work/ADBMS/flask/hello_flask/static', filename)


if __name__ == '__main__':
    test_fan_fic_v3.run(debug=True)
