import requests
import json

# Replace the URL with the endpoint you want to send the POST request to
url = 'https://example.com/api/endpoint'

# Replace the data_dict with the JSON data you want to send in the request body
data_dict = {
    "key1": "value1",
    "key2": "value2"
}

# Convert the dictionary to a JSON string
json_data = json.dumps(data_dict)

# Set the headers to indicate that you are sending JSON data
headers = {'Content-Type': 'application/json'}

# Make the POST request
response = requests.post(url, data=json_data, headers=headers)

# Print the response status code and content
print('Status Code:', response.status_code)
print('Response Content:', response.text)
