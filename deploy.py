from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import io
import cv2
from io import BytesIO
from sklearn.metrics import accuracy_score

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
app = Flask(__name__)

# Load the trained model
model = load_model('model.h5')
class_names = ['metal', 'glass', 'organic', 'paper', 'cardboard', 'plastic']

# Function to preprocess the image
def preprocess_image(image_path):
    
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format

    # Konversi ke citra grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Ekualisasi histogram pada citra grayscale
    equalized_image = cv2.equalizeHist(gray_image)

    # Konversi kembali ke citra RGB
    equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2RGB)

    image = cv2.resize(equalized_image_rgb, (224, 224))  # Resize the image to the input size of the model
    image = image / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add a batch dimension
    return image

# API endpoint for prediction
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def predict():
    image_file = request.files['image']
    image_path = "./images/" + image_file.filename
    image_file.save(image_path)
    # print(image_file.filename)

    # Check if the file is an image
    if image_file == '':
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)
    
    # Make a prediction
    predictions = model.predict(preprocessed_image)
    # Get the predicted class index
    predicted_class_index = np.argmax(predictions)

    # Get the predicted class name
    predicted_class_name = class_names[predicted_class_index]

    confidence_score = predictions[0][predicted_class_index]

    #calculate accuracy
    # true_labels = load_true_labels()  # This function should load true labels
    
    # # Assuming you have predicted labels in `predicted_class_index`
    # predicted_labels = [class_names[idx] for idx in predicted_class_index]
    
    # # Calculate accuracy
    # accuracy = accuracy_score(true_labels, predicted_labels)
    
    # Return the predicted class and accuracy
    return render_template('index.html', prediction=predicted_class_name,accuracy=confidence_score)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
