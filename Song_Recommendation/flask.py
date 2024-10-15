from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    mood = data['mood']
    
    # Use your model to get a song recommendation
    recommended_song = recommend("cry")
    
    return jsonify({'song': recommended_song})

if __name__ == '__main__':
    app.run(debug=True)
