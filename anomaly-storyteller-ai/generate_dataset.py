import os
import pandas as pd
import random
from datetime import datetime, timedelta

# Ensure the data directory exists
data_dir = "anomaly-storyteller-ai/data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Settings
start_date = datetime(2025, 1, 1)
days = 30
locations = [
    {"city": "Pittsburgh", "state": "PA"},
    {"city": "Philadelphia", "state": "PA"},
    {"city": "Chicago", "state": "IL"}
]
device_types = ["Scanner A", "Scanner B", "Scanner C"]
store_chains = ["MegaMart", "QuickStop", "IDMaxx", "FastScan", "RetailX"]

# Function to generate a valid PA ID
def generate_pa_id(is_valid=True):
    id_digits = [random.randint(2, 9)]  # First digit (2-9)
    for _ in range(6):
        id_digits.append(random.randint(0, 9))  # Digits 2-7 (0-9)
    
    if is_valid:
        id_digits.append(11 - id_digits[0])  # Ensure checksum is valid
    else:
        id_digits.append((11 - id_digits[0] + random.randint(1,9) % 10)) # Force invalid checksum

    return "".join(map(str, id_digits))

# Function to generate a valid IL ID
def generate_il_id(is_valid=True):
    id_digits = [random.randint(1, 9)]  # First digit (1-9)
    for _ in range(2):
        id_digits.append(random.randint(0, 9))  # Digits 2 and 3 (0-9)

    if is_valid:
        if id_digits[0] % 2 == 1:  # If first digit is odd, fourth digit must be even
            id_digits.append(random.choice([0, 2, 4, 6, 8]))
        else:
            id_digits.append(random.randint(0, 9))  # If first digit is even, fourth digit can be anything
    else:
        if id_digits[0] % 2 == 1:
            id_digits.append(random.choice([1, 3, 5, 7, 9]))  # Force invalid checksum
        else:
            id_digits[0] += 1
            id_digits.append(random.choice([1, 3, 5, 7, 9])) # force invalid by making both odd


    for _ in range(4):
        id_digits.append(random.randint(0, 9))  # Digits 5-8 (0-9)
    return "".join(map(str, id_digits))

# Function to generate an ID
def generate_id(state, is_valid=True):
    if state == "PA":
        return generate_pa_id(is_valid)
    elif state == "IL":
        return generate_il_id(is_valid)
    else:
        return "".join(map(str, [random.randint(0, 9) for _ in range(8)]))  # Other states

# Generate dataset
data = []
for day in range(days):
    for hour in range(9, 17):
        for loc in locations:
            city, state = loc["city"], loc["state"]
            store = random.choice(store_chains)
            device = random.choice(device_types)

            # Determine the base number of unique IDs scanned that hour
            base_unique_ids = random.randint(5, 15)

            # Inject anomalies: too many/few unique IDs scanned in one hour
            if random.random() < 0.02:
                base_unique_ids *= random.randint(20, 40)
            elif random.random() > 0.98:
                base_unique_ids = random.randint(0, 3)

            unique_ids = []
            for _ in range(base_unique_ids):
                is_valid = random.random() >= 0.02  # 2% chance of invalid ID

                if is_valid:
                    id_number = generate_id(state, True)
                else:
                    id_number = generate_id(state, False)  # Inject invalid checksum anomalies!

                unique_ids.append((id_number, not is_valid))  # Store ID and validity

            # Determine how often each ID is scanned
            scan_events = []
            for id_number, is_invalid in unique_ids:
                scans = 1
                if random.random() < 0.01:
                    scans *= random.randint(4, 10)  # Anomaly: One ID scanned too many times

                scan_events.append((id_number, scans, is_invalid))

            # Save the data for each unique ID scanned
            for id_number, scans, is_invalid in scan_events:
                data.append({
                    "date": (start_date + timedelta(days=day)).date(),
                    "hour": hour,
                    "location": city,
                    "state": state,
                    "store_name": store,
                    "device_type": device,
                    "id_number": id_number,
                    "is_invalid_id": is_invalid,
                    "scan_count": scans
                })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv(os.path.join(data_dir, "barcode_scans.csv"), index=False)

print(f"✅ Dataset generated with {len(df)} rows and saved to {os.path.join(data_dir, 'barcode_scans.csv')}")

#generate the context dataset for storyteller AI

# Define the lists for known issues and policy changes
known_issues = [
    "Scanner lag reported", 
    "No issues",
    "Staff shortage", 
    "No issues",
    "Software update pending", 
    "No issues",
    "No issues"
]

policy_changes = [
    "Updated ID policy", 
    "None", 
    "New scanner model installed", 
    "None",
    "Strict ID verification", 
    "None",
    "None"
]

# Create a date range for 30 days starting 2025-01-01
dates = pd.date_range(start="2025-01-01", periods=30)

# Build the context data
data = []
for date in dates:
    for loc in locations:
        city, state = loc["city"], loc["state"]
        store = random.choice(store_chains)
        device = random.choice(device_types)
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "location": city,
            "state": state,
            "store_name": store,
            "device_type": device,
            "known_issues": pd.Series(known_issues).sample(1).iloc[0],
            "policy_change": pd.Series(policy_changes).sample(1).iloc[0]
        })

# Create a DataFrame
df_context = pd.DataFrame(data)

# Define the data directory (adjust as needed)
data_dir = "anomaly-storyteller-ai/data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Save to CSV
context_data_path = os.path.join(data_dir, "context_data.csv")
df_context.to_csv(context_data_path, index=False)

print("✅ context_data.csv generated at:", context_data_path)
