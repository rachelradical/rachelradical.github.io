import os
import json
import time
import pandas as pd
import subprocess
import sys

# Auto-install OpenAI package if missing
try:
    import openai
except ModuleNotFoundError:
    print("🔹 OpenAI package not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai==0.28"])
    import openai

# Configure OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", "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")  # Replace with your API key if necessary

# Define data directory
data_dir = "anomaly-storyteller-ai/data"

# Define file paths for anomalies and context data
storyteller_data_path = os.path.join(data_dir, "storyteller_data.json")
context_data_path = os.path.join(data_dir, "context_data.csv")

# Load detected anomalies
try:
    with open(storyteller_data_path, "r") as f:
        anomalies = json.load(f)
except FileNotFoundError:
    print(f"Error: {storyteller_data_path} not found.")
    anomalies = []
    exit()

# Load contextual information
try:
    context_df = pd.read_csv(context_data_path)
except FileNotFoundError:
    print(f"Error: {context_data_path} not found.")
    context_df = pd.DataFrame()
    exit()

# Function to find context for an anomaly based on location, store, and date
def find_context(row):
    if context_df.empty:
        return {}
    match = context_df[
        (context_df["location"] == row["location"]) &
        (context_df["store_name"] == row["store_name"]) &
        (context_df["date"] == row["date"])
    ]
    if not match.empty:
        return match.iloc[0].to_dict()
    return {}

# Attach context to each anomaly
for anomaly in anomalies:
    anomaly["context"] = find_context(anomaly)

# Function to generate a descriptive anomaly explanation using GPT-3.5 Turbo
def generate_story(anomaly):
    # Build a description string based on available anomaly fields
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
    delay = 2  # seconds
    while retry_count > 0:
        try:
            # New interface: include a system message for context
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # exponential backoff
                retry_count -= 1
            else:
                print(f"Error generating story: {e}")
                return "Error generating explanation."
    print("Max retries exceeded. Unable to generate explanation.")
    return "Error generating explanation."

# Generate explanations for each anomaly
if anomalies:
    for anomaly in anomalies:
        anomaly["explanation"] = generate_story(anomaly)

# Save the updated anomalies with explanations to a JSON file
output_path = os.path.join(data_dir, "storyteller_output.json")
with open(output_path, "w") as f:
    json.dump(anomalies, f, indent=4)

print(f"✅ AI storyteller data saved with explanations to {output_path}.")
