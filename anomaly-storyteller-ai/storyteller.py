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
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openai"])
    import openai

from openai import OpenAI
# Set API key from environment variable or hardcoded (replace with your key)
api_key = os.getenv
client = openai.OpenAI(api_key=api_key)

# Define data directory
data_dir = "/workspaces/rachelradical.github.io/anomaly-storyteller-ai/data"

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

# Group anomalies by date & location to reduce API calls
grouped_anomalies = {}
for anomaly in anomalies:
    key = (anomaly["date"], anomaly["location"])
    if key not in grouped_anomalies:
        grouped_anomalies[key] = []
    grouped_anomalies[key].append(anomaly)

# Function to generate **one** explanation per date/location batch
def generate_story(date, location, anomalies_list):
    anomaly_summaries = []
    for anomaly in anomalies_list:
        if anomaly.get("checksum_anomalies", False):
            anomaly_type = "Checksum Anomaly (Invalid ID format)"
        elif anomaly.get("scan_count_anomaly", False):
            anomaly_type = "Scan Count Anomaly (Too many/few scans)"
        else:
            anomaly_type = "Unknown Anomaly"

        summary = f"- Store: {anomaly.get('store_name', 'N/A')}, Device: {anomaly.get('device_type', 'N/A')}, ID: {anomaly.get('id_number', 'N/A')}, Type: {anomaly_type}"
        anomaly_summaries.append(summary)

    # Generate a **single** API request per batch of anomalies
    prompt = f"""
You are an AI assistant analyzing barcode scan anomalies.
A batch of anomalies was detected on {date} in {location}.

Detected Anomalies:
{chr(10).join(anomaly_summaries)}

Provide a **single**, concise explanation of potential causes for these anomalies. 
If an anomaly corresponds with a potential cause from the context provided, it is likely not fraudulent.
If there are checksum anomalies or repeated scans of unique IDs, and the context data provides no reasonable explanation, the anomaly should be highlighted as needing to be investigated for potential fraud.
"""

    retry_count = 3
    delay = 2  # seconds
    while retry_count > 0:
        try:
            # Use the new OpenAI API syntax
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
                retry_count -= 1
            else:
                print(f"Error generating story: {e}")
                return "Error generating explanation."

    print("Max retries exceeded. Unable to generate explanation.")
    return "Error generating explanation."

# Generate explanations for each grouped batch instead of individual anomalies
batch_explanations = {}
for (date, location), anomalies_list in grouped_anomalies.items():
    print(f"Processing anomalies for {date} in {location}...")
    batch_explanations[(date, location)] = generate_story(date, location, anomalies_list)

# Attach batch explanations back to each anomaly
for anomaly in anomalies:
    anomaly["explanation"] = batch_explanations.get((anomaly["date"], anomaly["location"]), "No explanation available.")

# Save the updated anomalies with explanations to a JSON file
output_path = os.path.join(data_dir, "storyteller_output.json")
with open(output_path, "w") as f:
    json.dump(anomalies, f, indent=4)

print(f"✅ AI storyteller data saved with explanations to {output_path}.")
