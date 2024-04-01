
# Poof: Web Scraping and Data Mining Utility
[![Python package](https://github.com/Zaydo123/poof/actions/workflows/python-package.yml/badge.svg)](https://github.com/Zaydo123/poof/actions/workflows/python-package.yml) 

## Overview

**Poof** is a comprehensive web scraping library designed for versatility and ease of use. It provides a robust set of tools for extracting data from websites, enabling users to gather valuable insights and information for a wide range of applications. It provides advanced features such as realistic user-agent generation and proxy management to enhance scraping efficiency and avoid detection. With **Poof**, users can effortlessly scrape web content, process data, and extract valuable information for analysis and decision-making.

## Key Features

- **Versatile User-Agent Generation:** Simulates requests from a wide range of devices and browsers to enhance the success rate in scraping diverse web content.
- **Abstracted Proxied Requests:** Simplifies the process of making requests through proxies by encapsulating the necessary configurations within the library.
- **Robust Proxy Management:** Incorporates advanced proxy testing and handling, including support for HTTP, HTTPS, SOCKS4, and SOCKS5 proxies, to overcome access restrictions and maintain anonymity.

## Getting Started

Embrace the power of Poof for your web scraping needs. Its user-friendly design, combined with powerful scraping capabilities, makes it an essential tool for any data-driven task or project.


### Installation
~~poof can be installed via pip:~~

```bash
~pip install poof_util
```

(Not yet available on PyPi)

### Usage

Basic Usage: 
```python
from poof_util import ProxyPool, Proxy, RequestSender

# Initialize a proxy pool
pool = ProxyPool()

# Load proxies from a file
pool.read_file('proxies.txt') # Optional: specify the proxy type (http, https, socks4, socks5) - default is http

# Add a proxy manually - Proxy(ip, port, username, password, protocol, speed, status)
pool.add(Proxy('127.0.0.1', '9050', 'user', 'pass', 'socks5', 100, 'active'))

# Print the number of proxies in the pool
print(pool.size())

# Initialize a request sender with the proxy pool
s = RequestSender(pool,1) # 1 is the maximum number of request retries - defaults to 3 

# Make a request
response = s.send_request('get', 'http://localhost:3000/ip') # Returns a requests.Response object or raises an exception on failure

# Print the response
print(response.text)
```
more examples to be added soon.
---

Download and integrate **Poof** into your workflow to transform how you interact with web data.

For more information and to download Poof, visit [GitHub Repository](https://github.com/Zaydo123/poof).
