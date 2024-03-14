import threading
import time
from flask import Flask, request, jsonify, redirect
from flask_sock import Sock as FlaskWSocket
from simple_websocket.ws import Server
import json

# https://github.com/miguelgrinberg/flask-sock
app = Flask(__name__)

app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 10}
wsock = FlaskWSocket(app)

# Initialize an empty list to store image links
image_queue = []
ws_client_list: list[Server] = [] 

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


def image_url_sender():
    while True:
        time.sleep(0.1)
        # print("Tick")
        while not image_queue:
            time.sleep(0.3)
            pass
        clients = ws_client_list.copy()
        if clients:
            
            images_to_return = image_queue[:]
            image_queue.clear()
            
            for client in clients:
                try:
                    # images_to_return = image_queue[:]
                    # image_queue.clear()
                    _payload = json.dumps({'images': images_to_return})
                    print("[WS PAYLOAD]", _payload)
                    client.send(_payload)
                except Exception as e:
                    print("[WS EXCEPT]", e)
                    ws_client_list.remove(client)


@wsock.route('/frontendws')
def wsock_frontend_com(ws: Server):
    print("[WS] New websocket connection!")
    print(ws.mode)
    ws_client_list.append(ws)
    while True:
        data = ws.receive(0)
        time.sleep(0.5)
        if data:
            # if data is None: data = ""
            print()
            print(f"[WS DATA {type(data)}]", data)
            print()
            if data.strip() == 'stop':
                ws.close(message="1000 client request - stop")
                ws_client_list.remove(ws)
                break
    print("[WS] Disconnected!")
    
@app.route('/')
def goto_correct():
    return redirect('/static/index.html')

if __name__ == '__main__':
    t = threading.Thread(target=image_url_sender)
    t.daemon = True
    t.start()
    app.run(debug=False)
