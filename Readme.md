


# Website Attack Tool

This is a Python-based command-line tool designed for testing the performance and resilience of web servers. It allows users to send multiple HTTP requests to a specified URL using various methods (GET or POST) and can utilize proxy servers to mask the source of the requests.

## Features

- **Asynchronous Requests**: Utilizes `asyncio` and `aiohttp` for efficient handling of multiple requests.
- **User-Agent Rotation**: Randomly selects user agents from a predefined list to simulate real browser requests.
- **Proxy Support**: Allows for the use of HTTP and SOCKS proxies stored in a `proxy.txt` file.
- **Customizable Parameters**: Specify the number of requests, request method, payload for POST requests, and duration of the attack.
- **Real-time Statistics**: Displays real-time statistics of successful and failed requests during execution.

## Installation

### Prerequisites

Make sure you have Python 3.7 or higher installed on your machine. You will also need to install the required Python packages. You can do this using pip:

```bash
pip install aiohttp
```

### Usage

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/kabir403/ura
   cd ura
   ```

2. Create a `ua.txt` file in the same directory and add your desired User-Agent strings, each on a new line.

3. (Optional) Create a `proxy.txt` file in the same directory and add your proxy addresses in the following format:

   ```
   http://152.26.231.93:9443
   socks4://192.252.208.67:14287
   ```

4. Run the tool with the following command:

   ```bash
   python ura.py
   ```

5. Follow the prompts to enter the required information:

   - **URL**: The target URL (mandatory).
   - **Threads**: The number of concurrent requests (mandatory).
   - **Method**: Choose either GET or POST (mandatory).
   - **Payload**: Input the payload for POST requests (mandatory for POST).
   - **Time**: Duration of the attack in seconds (mandatory).
   - **Proxy**: Choose whether to use proxies (Y/N, default is N).

## Example

```bash
python attacker.py
```

```
  _    _ _____                      _ 
 | |  | |  __ \     /\        /\   | |
 | |  | | |__) |   /  \      /  \  | |
 | |  | |  _  /   / /\ \    / /\ \ | |
 | |__| | | \ \  / ____ \  / ____ \|_|
  \____/|_|  \_\/_/    \_\/_/    \_(_)

URL (mandatory): http://example.com
Threads (mandatory): 100
Method (GET/POST mandatory): GET
Payload (mandatory for POST): 
Time (mandatory): 60
Use Proxies? (Y/N, default N): N
```

## Disclaimer

This tool is intended for educational purposes and should only be used in environments where you have explicit permission to perform load testing. Unauthorized use against servers without consent may be illegal and unethical.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

