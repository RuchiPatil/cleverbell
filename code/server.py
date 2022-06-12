from flask import Flask, request, Response, send_file, send_from_directory
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)

new_name = 'stst'
# route http posts to this method

@app.route('/saveimage/<string:name>', methods=['POST'])
def test(name):
    global new_name
    new_name = name
    r = request
    # convert string of image data to uint8
    print(name)
    nparr = np.frombuffer(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite(f"images/{name}.jpg", img)

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

#UPON REQUEST sending image to Receiver (and then deleteing image 1 minute after sending)
@app.route("/lol_idk")
def lol_idk():
    send_from_directory('./', f"{new_name}.jpg", as_attachment=True)
    return Response(response=new_name, mimetype="text")
    #return send_file(img, mimetype='image/gif', as_attachment=True)
#UPON REQUEST receiving image from Sender
#send to client
@app.route("/get_image", methods=['GET'])
def get_image():
    r = request
    print(f"line 24 new_name: {new_name}\n")
    img = cv2.imread(f"images/{new_name}.jpg")
    print("line 47")
    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    print(f"img_enc: {type(img_encoded)}\nimg:{img_encoded}")

    response = {'name': new_name,
                'img': img_encoded.tostring()
                }
    responsep = jsonpickle.encode(response)
    return Response(response=responsep, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
