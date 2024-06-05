import aiohttp
import asyncio
import time
from datetime import datetime

# Set the URL of the website you want to test
URL = "https://scriptmakeryt.netlify.app/"

# Number of simultaneous requests
CONCURRENT_REQUESTS = 100

# Statistics
total_requests = 0
successful_requests = 0
failed_requests = 0

async def send_request(session):
    global total_requests, successful_requests, failed_requests
    try:
        async with session.get(URL) as response:
            total_requests += 1
            if response.status == 200:
                successful_requests += 1
            else:
                failed_requests += 1
    except Exception:
        total_requests += 1
        failed_requests += 1

async def load_test():
    global total_requests, successful_requests, failed_requests

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [send_request(session) for _ in range(CONCURRENT_REQUESTS)]
            await asyncio.gather(*tasks)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success_in_batch = min(successful_requests, CONCURRENT_REQUESTS)
            fail_in_batch = min(failed_requests, CONCURRENT_REQUESTS)
            print(f"[{timestamp}] Requests {total_requests - CONCURRENT_REQUESTS + 1}-{total_requests}: Successful: {success_in_batch}, Failed: {fail_in_batch}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    print("Load test started.")
    try:
        asyncio.run(load_test())
    except KeyboardInterrupt:
        print("Load test stopped.")
        print(f"Final counts - Total requests: {total_requests}, Successful: {successful_requests}, Failed: {failed_requests}")
