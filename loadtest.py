import aiohttp
import asyncio
from datetime import datetime

# Set the URL of the website you want to test
URL = "https://scriptmakeryt.netlify.app/"

# Number of simultaneous requests
CONCURRENT_REQUESTS = 500  # Adjust this value as needed
PRINT_INTERVAL = 100  # Print statistics after every 100 requests

# Statistics
total_requests = 0
successful_requests_in_interval = 0
failed_requests_in_interval = 0

async def send_request(session):
    global total_requests, successful_requests_in_interval, failed_requests_in_interval
    try:
        async with session.get(URL) as response:
            total_requests += 1
            if response.status == 200:
                successful_requests_in_interval += 1
            else:
                failed_requests_in_interval += 1
                
            if total_requests % PRINT_INTERVAL == 0:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Requests {total_requests-PRINT_INTERVAL+1}-{total_requests}: Successful: {successful_requests_in_interval}, Failed: {failed_requests_in_interval}")
                successful_requests_in_interval = 0
                failed_requests_in_interval = 0
    except Exception:
        total_requests += 1
        failed_requests_in_interval += 1

async def load_test():
    global total_requests

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_request(session) for _ in range(CONCURRENT_REQUESTS)]
            await asyncio.gather(*tasks)
            await asyncio.sleep(1)

async def run_load_test():
    print("Load test started.")
    try:
        await load_test()
    except KeyboardInterrupt:
        print("Load test stopped.")
        print(f"Final counts - Total requests: {total_requests}, Successful: {total_requests - failed_requests_in_interval}, Failed: {failed_requests_in_interval}")

    # This code will actually start the load test in Google Colab
    await run_load_test()
