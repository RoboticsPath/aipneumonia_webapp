from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

dic = {0 : 'OK', 1 : 'NOT OK'}

model = load_model('model.h5')

model.make_predict_function()

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(150,150))
    i = image.img_to_array(i)/255.0
    i = i.reshape(-1, 150,150,1)
    px = model.predict(i)
    p=np.argmax(px, axis=1)
    return 'Initial Diagnosis: OK' if px[0][0] > 0.5 else 'Initial Diagnosins: NOK'

## # # routes
@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")

@app.route("/about")
def about_page():
    return "Done By: Amr Aboushousha & Lamees El-Bakr"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image']
        img_path = "static/" + img.filename	
        img.save(img_path)
        p = predict_label(img_path)
    return render_template("index.html", prediction = p, img_path = img_path)
    #return "okindex.html"

if __name__ =='__main__':
 	app.debug = True
 	app.run(debug = True)
