from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import subprocess
import os

app = Flask(__name__)
CORS(app)  # Enables CORS so your Angular UI can talk to the backend

# Load your trained model (make sure the file 'intrusion_model.h5' is in the same directory as app.py or provide its full path)
model = tf.keras.models.load_model('intrusion_model.h5')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        # Trigger the NS3 simulation. Adjust the path as needed.
        result = subprocess.check_output(["./ns3", "run", "scratch/NS3_simulation"], cwd="/home/pb/ns-3-dev/ns-allinone-3.43/ns-3.43")
        return jsonify({"status": "success", "output": result.decode('utf-8')})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/process_pcap', methods=['POST'])
def process_pcap():
    file = request.files.get('pcap')
    if not file:
        return jsonify({"status": "error", "message": "No file provided"})
    pcap_path = os.path.join("/tmp", file.filename)
    file.save(pcap_path)
    # (Process the pcap file here using Python libraries like Scapy.)
    extracted_data = {"total_packets": 100, "avg_packet_size": 512}
    return jsonify({"status": "success", "data": extracted_data})

@app.route('/predict', methods=['POST'])
def predict():
    # Get feature data from the POST request
    features = request.json.get("features")
    
    if features is None:
        return jsonify({"status": "error", "message": "No features provided"}), 400

    # Convert features into a NumPy array and reshape to 2D array
    input_data = np.array(features).reshape(1, -1)
    
    # Use the loaded model to get a prediction
    prediction = model.predict(input_data)[0][0]
    
    # Define a threshold for classification (0.5 is common for binary classification)
    intrusion_detected = prediction > 0.5
    
    # Return the prediction as a JSON response
    return jsonify({
        "status": "success",
        "prediction": {
            "intrusion_detected": bool(intrusion_detected),
            "confidence": float(prediction)
        }
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "running", "details": "All systems nominal."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
