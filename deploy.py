from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import cv2
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('model-densenet121.h5')

class_names = ['cardboard', 'glass', 'metal', 'organic', 'paper', 'plastic']

# Function to preprocess the image
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert image to RGB format

    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Histogram equalization on grayscale image
    equalized_image = cv2.equalizeHist(gray_image)

    # Convert back to RGB
    equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2RGB)

    image = cv2.resize(equalized_image_rgb, (224, 224))  # Resize the image to the input size of the model

    # Save the preprocessed image
    preprocessed_image_path = os.path.join('static', 'preprocessed_images', os.path.basename(image_path))
    cv2.imwrite(preprocessed_image_path, cv2.cvtColor(equalized_image_rgb, cv2.COLOR_RGB2BGR))

    image = image / 255.0  # Normalize the image
    image = np.expand_dims(image, axis=0)  # Add a batch dimension
    return image, preprocessed_image_path

# API endpoint for prediction
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_file = request.files['image']
    image_path = os.path.join('static', 'images', image_file.filename)
    image_file.save(image_path)

    # Check if the file is an image
    if image_file == '':
        return jsonify({'error': 'No image uploaded'}), 400
    
    # Preprocess the image
    preprocessed_image, preprocessed_image_path = preprocess_image(image_path)
    
    # Make a prediction
    predictions = model.predict(preprocessed_image)

    # Get predictions for all classes
    results = {class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}

    # Sort the results by probability in descending order
    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    # Get the predicted class name and confidence score
    predicted_class_index = np.argmax(predictions)
    predicted_class_name = class_names[predicted_class_index]
    confidence_score = predictions[0][predicted_class_index]

    return render_template('index.html', prediction=predicted_class_name, accuracy=confidence_score, preprocessed_image_path=preprocessed_image_path, class_probabilities=sorted_results)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
