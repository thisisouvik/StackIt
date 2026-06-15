import requests
city = 'london'
api_url = 'https://api.api-ninjas.com/v1/airquality?city={}'.format(city)
response = requests.get(api_url, headers={'X-Api-Key': 'Axgnxoq7oecPSb/xeg1VVQ==8CvCdygsj7NW7gAX'})
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
    # To run this API, ensure you have the 'requests' library installed.
    # You can install it using pip if not already installed:
    # pip install requests