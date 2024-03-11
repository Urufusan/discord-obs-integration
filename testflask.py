from flask import Flask, request, jsonify, redirect
# https://github.com/miguelgrinberg/flask-sock
app = Flask(__name__)

# Initialize an empty list to store image links
image_queue = []

# Endpoint to add a new image link to the queue
@app.route('/newimage', methods=['POST'])
def new_image():
    # Get the image link from the request parameters
    # print(request.headers)
    imagelinks = request.json
    print(imagelinks)
    # return 'OK', 200
    if imagelinks:
        # Append the image link to the queue
        for _src_url_i in imagelinks:
            image_queue.append(_src_url_i)
        return jsonify({'message': 'Image link added to the queue'}), 200
    else:
        return jsonify({'error': 'No image link provided'}), 400

# Endpoint to get all the images in the queue
@app.route('/getimages', methods=['GET'])
def get_images():
    # Get the images from the queue and empty the queue
    images_to_return = image_queue[:]
    image_queue.clear()
    # Return the images in JSON format
    return jsonify({'images': images_to_return}), 200

@app.route('/')
def goto_correct():
    return redirect('/static/index.html')

if __name__ == '__main__':
    app.run(debug=False)
