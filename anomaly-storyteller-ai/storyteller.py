import os
import pandas as pd
import openai

# 🔹 Ensure OpenAI API key is set (replace with your actual API key)
openai.api_key = "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"

# 🔹 Load the detected anomalies dataset
anomaly_file = "data/detected_anomalies.csv"

if not os.path.exists(anomaly_file):
    print("❌ No anomaly data found! Run anomaly detection first.")
    exit()

df = pd.read_csv(anomaly_file)

# 🔹 Analyze common trends in the anomalies
anomaly_summary = df.groupby(["location", "device_type"]).agg({
    "scan_count": ["mean", "max", "count"]
}).reset_index()

# Rename columns for clarity
anomaly_summary.columns = ["location", "device_type", "avg_scan_count", "max_scan_count", "anomaly_count"]

# Sort by most frequent anomalies
anomaly_summary = anomaly_summary.sort_values(by="anomaly_count", ascending=False)

# 🔹 Convert structured data into text format for AI
summary_text = []
for _, row in anomaly_summary.iterrows():
    summary_text.append(
        f"- {row['location']} (Device: {row['device_type']}) had {row['anomaly_count']} anomalies. "
        f"Avg scans: {row['avg_scan_count']:.1f}, Max scans: {row['max_scan_count']}."
    )

summary_text = "\n".join(summary_text)

# 🔹 Generate AI-driven report
prompt = f"""
You are an AI data analyst reviewing barcode scan anomaly data. Based on the structured summary below, 
write a **concise, data-driven anomaly report**.

**Data Summary:**
{summary_text}

Your report should include:
1️⃣ General trends in the anomalies.
2️⃣ Top locations/devices with the most anomalies.
3️⃣ Any time-based trends (e.g., spikes in afternoons, Mondays, etc.).
4️⃣ A concise, factual conclusion.

**DO NOT SPECULATE. Only use data from the summary.**
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

# 🔹 Save the AI-generated report
story = response["choices"][0]["message"]["content"]

report_path = "data/anomaly_report.txt"
with open(report_path, "w") as f:
    f.write(story)

print("\n📊 **ANOMALY REPORT GENERATED!** 📊\n")
print(story)
print(f"\n✅ Report saved to {report_path}")

