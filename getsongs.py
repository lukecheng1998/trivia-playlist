import requests
# This file will get the songs and convert to a json file
url = 'https://en.wikipedia.org/wiki/List_of_Billboard_Year-End_number-one_singles_and_albums'
# Make a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the content of the webpage
    print(response.text)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code}")