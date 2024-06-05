import requests

def send_requests(url, num_requests):
    for i in range(num_requests):
        try:
            response = requests.get(url)
            print(f"Request {i+1}: Status Code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Request {i+1}: Failed with error: {e}")

if __name__ == "__main__":
    url = input("Enter the website URL: ")
    num_requests = int(input("Enter the number of requests to send: "))
    
    send_requests(url, num_requests)
