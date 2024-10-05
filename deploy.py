from flask import Flask, request, jsonify, render_template
import numpy as np
import os
import cv2
import tensorflow as tf
import resource

# Mengatur batasan jumlah proses
soft, hard = resource.getrlimit(resource.RLIMIT_NPROC)
resource.setrlimit(resource.RLIMIT_NPROC, (soft, hard))
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
app = Flask(__name__)

try:
    model = tf.keras.models.load_model('model-densenet121.h5')
except Exception as e:
    print(f"Error loading model: {e}")

class_names = ['cardboard', 'glass', 'metal', 'organic', 'paper', 'plastic']

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  

    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    equalized_image = cv2.equalizeHist(gray_image)

    equalized_image_rgb = cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2RGB)

    image = cv2.resize(equalized_image_rgb, (224, 224))  

    preprocessed_image_path = os.path.join('static', 'preprocessed_images', os.path.basename(image_path))
    cv2.imwrite(preprocessed_image_path, cv2.cvtColor(equalized_image_rgb, cv2.COLOR_RGB2BGR))

    image = image / 255.0  
    image = np.expand_dims(image, axis=0) 
    return image, preprocessed_image_path

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    image_file = request.files['image']
    
    image_path = os.path.join('static', 'images', image_file.filename)
    image_file.save(image_path)

    if image_file == '':
        return jsonify({'error': 'No image uploaded'}), 400
    
    preprocessed_image, preprocessed_image_path = preprocess_image(image_path)
    
    predictions = model.predict(preprocessed_image)

    results = {class_names[i]: float(predictions[0][i]) for i in range(len(class_names))}

    sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    predicted_class_index = np.argmax(predictions)
    predicted_class_name = class_names[predicted_class_index]
    confidence_score = predictions[0][predicted_class_index]

    return render_template('index.html', prediction=predicted_class_name, accuracy=confidence_score, preprocessed_image_path=preprocessed_image_path, class_probabilities=sorted_results)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
