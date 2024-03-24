import threading
import time
from flask import Flask, request, jsonify, redirect
from flask_sock import Sock as FlaskWSocket
from simple_websocket.ws import Server
import json
import pprint
from dist_app_updater import is_outdated

# from io import StringIO
CON_HEADER_TEXT = """   ____        ____  __   _____
   / __ \      / __ \/ /_ / ___/
  / / / /_____/ / / / __ \\\__ \ 
 / /_/ /_____/ /_/ / /_/ /__/ / 
/_____/      \____/_.___/____/  
"""

class TerminalColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    ORANGE = '\033[33m'

    @staticmethod
    def terminalpaint(color):
        if isinstance(color, str):
            if color.startswith("#"):
                color = color[1:]
            r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        elif isinstance(color, tuple) and len(color) == 3:
            r, g, b = color
        else:
            raise ValueError("Invalid color format")
        
        color_code = f"\x1b[38;2;{r};{g};{b}m"
        return color_code

    def print_ctext(self, _text, color="#964bb4"):
        color_code = self.terminalpaint(color)
        # _str_io_buf = StringIO()
        # pprint.pprint(object=_text, stream=_str_io_buf)
        # _raw_pp_str = _str_io_buf.getvalue()
        # del _str_io_buf
        _raw_pp_str = pprint.pformat(object=_text)
        _raw_pp_str = _raw_pp_str.strip()
        if _raw_pp_str:
            if _raw_pp_str.endswith("'"):
                _raw_pp_str = _raw_pp_str.strip("'")
            elif _raw_pp_str.endswith("\""):
                _raw_pp_str = _raw_pp_str.strip("\"")

            print(f"{self.terminalpaint(color)}{_raw_pp_str}{self.ENDC}")

tc = TerminalColors()
printfc = tc.print_ctext

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

@app.route('/specialmessage', methods=['POST'])
def specialmesssage():
    _specialmsg = request.json
    clients = ws_client_list.copy()
    if clients:
        for client in clients:
            try:
                tc.print_ctext(f"[WS SPEC MSG] {_specialmsg}", color="#ffdc3e")
                client.send(json.dumps(_specialmsg))
                return "OK", 200
            except Exception as e:
                tc.print_ctext(f"[WS EXCEPT] {e}", color="#ff4444")
                ws_client_list.remove(client)
                return "WS FAIL", 500
    return "NO CLIENTS", 503

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
                    print(f"{tc.terminalpaint('#339bbb')}[WS PAYLOAD]{tc.ENDC}", _payload)
                    client.send(_payload)
                except Exception as e:
                    tc.print_ctext(f"[WS EXCEPT] {e}", color="#ff4444")
                    ws_client_list.remove(client)


@wsock.route('/frontendws')
def wsock_frontend_com(ws: Server):
    tc.print_ctext(f"[WS] New websocket connection! - {ws.mode}", color="#3dfa4d")
    # print(ws.mode)
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
            elif data.strip().startswith("@WSCONNECT"):
                if is_outdated():
                    ws.send(json.dumps({"spec_message": f"Discord overlay is not up-to-date!<br>please update!"}))
                    
    tc.print_ctext("[WS] Disconnected!", color="#ff4444")
    
@app.route('/')
def goto_correct():
    return redirect('/static/index.html')

if __name__ == '__main__':
    t = threading.Thread(target=image_url_sender)
    t.daemon = True
    t.start()
    print(tc.terminalpaint("#964bb4"), CON_HEADER_TEXT, tc.ENDC)
    app.run(debug=False)
