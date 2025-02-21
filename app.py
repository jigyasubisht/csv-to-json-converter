import os
import pandas as pd
import json
import re
from flask import Flask, render_template, request, send_file
from threading import Thread

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "processed_json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Function to Convert CSV to JSON
def convert_csv_to_json(csv_path, json_path):
    df = pd.read_csv(csv_path)

    # Drop unnecessary index column
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Add a new column with index format
    df.insert(0, '', range(len(df)))

    # Convert DataFrame to JSON
    json_data = df.to_json(orient='records', indent=4)

    # Format JSON output
    json_data = re.sub(r'("\w*":)(?! \d)', r'\1 ', json_data)

    # Save to JSON file
    with open(json_path, 'w') as json_file:
        json_file.write(json_data)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file uploaded.")

        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No selected file.")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        json_path = os.path.join(OUTPUT_FOLDER, f"{os.path.splitext(file.filename)[0]}.json")

        file.save(file_path)

        # Run conversion in a separate thread
        thread = Thread(target=convert_csv_to_json, args=(file_path, json_path))
        thread.start()

        return render_template("index.html", message="Processing file. Please wait...", download_url=f"/download/{os.path.basename(json_path)}")

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
