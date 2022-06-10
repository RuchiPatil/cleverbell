from flask import Flask, request, Response, send_file, send_from_directory
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)

#UPON REQUEST receiving image from Sender
@app.route('/getNoteText',methods=['GET','POST'])
def GetNoteText():
    if request.method == 'POST':
        file = request.files['pic']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        processImage(filename)
    else:
        return "Y U NO USE POST?"
# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('download2.jpg', img)

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

#UPON REQUEST sending image to Receiver (and then deleteing image 1 minute after sending)
@app.route("/get_image")
def get_image():

    return send_from_directory('./', 'get.jpg', as_attachment=True)
    #return send_file(img, mimetype='image/gif', as_attachment=True)



# start flask app
app.run(host="0.0.0.0", port=5000)
