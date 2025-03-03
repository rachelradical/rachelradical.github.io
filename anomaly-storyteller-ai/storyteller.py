import os
import json
import time 
import pandas as pd

# Try importing google-generativeai, install if missing
try:
    import google.generativeai as genai
except ModuleNotFoundError:
    print("🔹 google-generativeai not found. Installing...")
    os.system("pip install google-generativeai")
    import google.generativeai as genai  # Try again after installation

# 🔹 Step 1: Load API Key
genai.configure(api_key="AIzaSyAhWpMYn8HuzoNhD08NwYRoLI_NZBdUvDI")


# Define data directory
data_dir = "anomaly-storyteller-ai/data"

# 🔹 Step 2: Load Anomalies & Context Data
storyteller_data_path = os.path.join(data_dir, "storyteller_data.json")
context_data_path = os.path.join(data_dir, "context_data.csv")

# Load detected anomalies
try:
    with open(storyteller_data_path, "r") as f:
        anomalies = json.load(f)
except FileNotFoundError:
    print(f"Error: {storyteller_data_path} not found.")
    anomalies = [] # prevent errors later
    exit() # exit because the main data is missing

# Load contextual information
try:
    context_df = pd.read_csv(context_data_path)
except FileNotFoundError:
    print(f"Error: {context_data_path} not found.")
    context_df = pd.DataFrame() # prevent errors later
    exit() # exit because the main data is missing

# 🔹 Step 3: Match Anomalies to Context
def find_context(row):
    """Finds relevant context for an anomaly based on location, store, or date."""
    if context_df.empty: #handle empty dataframes
        return {}

    match = context_df[
        (context_df["location"] == row["location"])
        & (context_df["store_name"] == row["store_name"])
    ]

    if not match.empty:
        return match.iloc[0].to_dict()  # Convert first match to a dictionary
    return {}

if anomalies: # only run if there is data
    for anomaly in anomalies:
        anomaly["context"] = find_context(anomaly)

# 🔹 Step 4: Generate AI Storytelling
def generate_story(anomaly):
    # Determine the anomaly description based on available fields:
    if anomaly.get("checksum_anomalies", False):
        anomaly_desc = "This is a checksum anomaly: the ID fails the expected checksum validation."
    elif anomaly.get("scan_count_anomaly"):
        anomaly_desc = "This is a scan count anomaly: the ID was scanned an abnormal number of times."
    else:
        anomaly_desc = "No specific anomaly type is indicated based on the available data."

    prompt = f"""
You are an AI assistant analyzing barcode scan anomalies.
Here is the detected anomaly:

- Date: {anomaly.get('date', 'N/A')}
- Hour: {anomaly.get('hour', 'N/A')}
- Location: {anomaly.get('location', 'N/A')}
- Store: {anomaly.get('store_name', 'N/A')}
- Device: {anomaly.get('device_type', 'N/A')}
- ID Number: {anomaly.get('id_number', 'N/A')}
- Scan Count: {anomaly.get('scan_count', 'N/A')}

Additional Details:
- Calculated Valid ID: {anomaly.get('calculated_valid_id', 'N/A')}
- Checksum Anomalies: {anomaly.get('checksum_anomalies', 'N/A')}
- Scan Count Z-Score: {anomaly.get('scan_count_z_score', 'N/A')}
- Scan Count Anomaly: {anomaly.get('scan_count_anomaly', 'N/A')}

Explanation: {anomaly_desc}

Provide a concise, data-driven explanation of what might be causing this anomaly, using only the information above.
    """

    retry_count = 3
    delay = 2  # Initial delay in seconds

    while retry_count > 0:
        try:
            response = genai.GenerativeModel("models/gemini-1.5-pro").generate_content(prompt)
            return response.text if response else "No explanation available."
        except Exception as e: #to handle quota limit
            if "429" in str(e):
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                retry_count -= 1
            else:
                print(f"Error generating story: {e}")
                return "Error generating explanation."

    print("Max retries exceeded. Unable to generate explanation.")
    return "Error generating explanation."

# 🔹 Step 5: Generate Explanations for Each Anomaly
if anomalies: #only run if there is data
    for anomaly in anomalies:
        anomaly["explanation"] = generate_story(anomaly)

# 🔹 Step 6: Save the Updated Anomalies with Explanations
if anomalies:
    for anomaly in anomalies:
        anomaly["explanation"] = generate_story(anomaly)
        time.sleep(1) #add a small delay between each call.

    print(f"✅ AI storyteller data saved with explanations to {output_path}.")
else:
    print("No anomaly data to process.")
