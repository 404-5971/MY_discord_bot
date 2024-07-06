import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time
import json

# Replace 'YOUR_API_TOKEN' with your actual AQICN API token
api_token = '921cd3bc9a84df5559fb056e1cdefcf218264117'
city = 'Los Angeles'

url = f'https://api.waqi.info/feed/{city}/?token={api_token}'

data_points = []

# Collect data for the past 1000 minutes (approximately 17 hours) at 10-minute intervals
for _ in range(86400):  # 1000 minutes / 10 minutes = 100 data points
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'ok':
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        aqi = data['data']['aqi']
        
        data_points.append({'time': current_time, 'aqi': aqi})
        print(f"Time: {current_time}, AQI: {aqi}")
    else:
        print("Error fetching data")
    
    # Wait for 10 minutes before the next request
    time.sleep(60)  # 600 seconds = 10 minutes

# Save the collected data to a JSON file
with open('aqi_data.json', 'w') as f:
    json.dump(data_points, f, indent=4)

# Extract timestamps and AQI values for plotting
timestamps = [datetime.strptime(point['time'], '%Y-%m-%d %H:%M:%S') for point in data_points]
aqi_values = [point['aqi'] for point in data_points]

# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(timestamps, aqi_values, marker='o', linestyle='-')
plt.xlabel('Time')
plt.ylabel('AQI Value')
plt.title('AQI Values for the Past 1000 Minutes')
plt.grid(True)
plt.show()