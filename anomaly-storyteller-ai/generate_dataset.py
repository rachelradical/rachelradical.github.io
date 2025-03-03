import os
import pandas as pd
import random
from datetime import datetime, timedelta

# Ensure the data directory exists
data_dir = "data"
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

# Function to generate a random 8-digit ID number
def generate_id(state):
    id_number = [random.randint(1, 9)]  # First digit should never be 0
    id_number += [random.randint(0, 9) for _ in range(7)]  # Rest are random

    # Apply checksum rules based on state
    if state == "PA":  # Pittsburgh & Philadelphia
        if (id_number[0] + id_number[7]) != 11:
            id_number[7] = 11 - id_number[0]
    elif state == "IL":  # Chicago
        if (id_number[0] * id_number[3]) % 2 != 0:
            id_number[3] = random.choice([0, 2, 4, 6, 8])

    return "".join(map(str, id_number))

# Inject anomalies (Invalid IDs)
def generate_invalid_id(state):
    id_number = [random.randint(1, 9)]
    id_number += [random.randint(0, 9) for _ in range(7)]

    # Ensure the ID **fails** the checksum for its state
    if state == "PA":
        if (id_number[0] + id_number[7]) == 11:
            id_number[7] = (id_number[7] + 2) % 10  # Force invalidity
    elif state == "IL":
        if (id_number[0] * id_number[3]) % 2 == 0:
            id_number[3] = random.choice([1, 3, 5, 7, 9])  # Force invalidity

    return "".join(map(str, id_number))

# Generate dataset
data = []
for day in range(days):
    for hour in range(9, 18):  # Business hours 9 AM to 5 PM
        for loc in locations:
            city, state = loc["city"], loc["state"]
            store = random.choice(store_chains)
            device = random.choice(device_types)

            # Generate mostly valid IDs, with **only 2-5% invalid ones**
            if random.random() < 0.03:  # Now ~3% invalid instead of 10-15%
                id_number = generate_invalid_id(state)
                is_invalid = True
            else:
                id_number = generate_id(state)
                is_invalid = False

            scan_count = random.randint(80, 200)  # Base scan count

            # Introduce store-based variations
            if store in ["MegaMart", "IDMaxx"]:
                scan_count *= random.uniform(1.1, 1.3)  # Slightly higher scan volume stores
            elif store in ["FastScan"]:
                scan_count *= random.uniform(0.7, 0.9)  # Slightly lower scan volume

            # Inject **scan frequency anomalies** using Z-score logic
            if random.random() < 0.02:  # 2% chance of a big spike
                scan_count *= random.randint(3, 6)
            elif random.random() < 0.02:  # 2% chance of a dip
                scan_count = random.randint(20, 50)

            data.append({
                "date": (start_date + timedelta(days=day)).date(),
                "hour": hour,
                "location": city,
                "state": state,
                "store_name": store,
                "device_type": device,
                "id_number": id_number,
                "is_invalid_id": is_invalid,  # True/False flag
                "scan_count": int(scan_count)  # Convert float to int
            })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv(os.path.join(data_dir, "barcode_scans.csv"), index=False)

print(f"✅ Dataset generated with {len(df)} rows and saved to data/barcode_scans.csv")

