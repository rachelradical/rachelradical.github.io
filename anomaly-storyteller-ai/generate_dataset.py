import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Ensure the data directory exists
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
# Settings
start_date = datetime(2024, 1, 1)
days = 30
locations = ['Pittsburgh', 'Philadelphia', 'Chicago']
device_types = ['Scanner A', 'Scanner B', 'Scanner C']

data = []

for day in range(days):
    for hour in range(9, 18):  # business hours 9 AM to 5 PM
        for location in locations:
            date = (start_date + timedelta(days=day)).date()
            device = random.choice(device_types)
            
            # Normal scan count
            scan_count = random.randint(100, 200)
            
            # Inject random anomalies
            if random.random() < 0.02:  # 2% chance of a big spike
                scan_count *= random.randint(3, 6)
            elif random.random() < 0.02:  # 2% chance of a dip
                scan_count = random.randint(20, 50)
            
            data.append({
                'date': date,
                'hour': hour,
                'location': location,
                'device_type': device,
                'scan_count': scan_count
            })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv('data/barcode_scans.csv', index=False)

print(f"Dataset generated with {len(df)} rows.")
