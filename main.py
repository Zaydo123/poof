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