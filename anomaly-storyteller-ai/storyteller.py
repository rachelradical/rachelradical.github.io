import os
import json
import pandas as pd
import google.generativeai as genai  # Gemini AI

# 🔹 Step 1: Load API Key
genai.configure(api_key=os.getenv("AIzaSyAhWpMYn8HuzoNhD08NwYRoLI_NZBdUvDI"))

# Define data directory
data_dir = "anomaly-storyteller-ai/data"

# 🔹 Step 2: Load Anomalies & Context Data
storyteller_data_path = os.path.join(data_dir, "storyteller_data.json")
context_data_path = os.path.join(data_dir, "context_data.csv")

# Load detected anomalies
with open(storyteller_data_path, "r") as f:
    anomalies = json.load(f)

# Load contextual information
context_df = pd.read_csv(context_data_path)

# 🔹 Step 3: Match Anomalies to Context
def find_context(row):
    """Finds relevant context for an anomaly based on location, store, or date."""
    match = context_df[
        (context_df["location"] == row["location"])
        & (context_df["store_name"] == row["store_name"])
    ]
    
    if not match.empty:
        return match.iloc[0].to_dict()  # Convert first match to a dictionary
    return {}

for anomaly in anomalies:
    anomaly["context"] = find_context(anomaly)

# 🔹 Step 4: Generate AI Storytelling
def generate_story(anomaly):
    """Uses Gemini AI to generate a human-readable explanation for an anomaly."""
    prompt = f"""
    You are an AI assistant analyzing barcode scan anomalies.
    Here is the detected anomaly:
    
    - Date: {anomaly['date']}
    - Hour: {anomaly['hour']}
    - Location: {anomaly['location']}
    - Store: {anomaly['store_name']}
    - Device: {anomaly['device_type']}
    - ID Number: {anomaly['id_number']}
    - Anomaly Type: {anomaly['anomaly_type']}
    - Scan Count: {anomaly['scan_count']}
    
    Additional Context:
    {anomaly['context']}
    
    Explain why this anomaly might be happening in simple terms.
    """
    
    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text if response else "No explanation available."

# 🔹 Step 5: Generate Explanations for Each Anomaly
for anomaly in anomalies:
    anomaly["explanation"] = generate_story(anomaly)

# 🔹 Step 6: Save the Updated Anomalies with Explanations
output_path = os.path.join(data_dir, "storyteller_output.json")
with open(output_path, "w") as f:
    json.dump(anomalies, f, indent=4)

print(f"✅ AI storyteller data saved with explanations to {output_path}.")

