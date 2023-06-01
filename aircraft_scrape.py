import os
import csv
import requests
import json

# Get the directory path of the script
dir_path = os.path.dirname(os.path.realpath(__file__))

# CSV output file
csv_path = os.path.join(dir_path, 'airports.csv')
with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = None
    offset = 0
    
    # Make API requests
    while True:
        url = 'https://openflights.org/php/apsearch.php'
        params = {'offset': offset}
        response = requests.post(url, data=params)
        try:
            airport_data = response.json()
        except json.decoder.JSONDecodeError as e:
            print('Error: ', e)
            offset += 10
            continue

        # If the end, break out of the loop
        if not airport_data['airports']:
            break

        # Write the header row to the CSV file first
        if writer is None:
            writer = csv.DictWriter(csvfile, fieldnames=airport_data['airports'][0].keys())
            writer.writeheader()

        # Write each airports as a new row in the CSV file
        for airport in airport_data['airports']:
            writer.writerow(airport)

        # Increment the offset by 10
        offset += 10
        print('Inserted row ', offset)
