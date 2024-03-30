import requests
import socks
import socket

class RequestSender:
    def __init__(self, proxy_pool, max_retries=3):
        self.proxy_pool = proxy_pool
        self.max_retries = max_retries

    def send_request(self, method, url, data=None, params=None, headers=None, custom_proxy=None, retries=0):
        if retries > self.max_retries:
            raise Exception('Max retries exceeded')

        with requests.Session() as session:
            proxy = custom_proxy if custom_proxy else self.get_proxy()
            if not self.setup_proxy(session, proxy, url.startswith('https')):
                return self.send_request(method, url, data, params, headers, retries=retries + 1)

            try:
                if method.lower() == 'get':
                    response = session.get(url, params=params, headers=headers, timeout=10)
                elif method.lower() == 'post':
                    response = session.post(url, data=data, headers=headers, timeout=10)
                else:
                    raise ValueError("Unsupported method")
                return response
            except requests.RequestException:
                # On failure, retry with a different proxy
                return self.send_request(method, url, data, params, headers, retries=retries + 1)

    def send_get_request(self, url, params=None, headers=None, custom_proxy=None):
        return self.send_request('get', url, params=params, headers=headers, custom_proxy=custom_proxy)

    def send_post_request(self, url, data=None, headers=None, custom_proxy=None):
        return self.send_request('post', url, data=data, headers=headers, custom_proxy=custom_proxy)

    def setup_proxy(self, session, proxy, is_https):
        protocol = proxy.get_protocol()
        proxy_auth = proxy.get_auth()
        proxy_address = f"{proxy.get_ip()}:{proxy.get_port()}"

        if protocol in ["socks4", "socks5"]:
            socks_type = socks.SOCKS5 if protocol == "socks5" else socks.SOCKS4
            if proxy_auth:
                socks.set_default_proxy(socks_type, proxy.get_ip(), int(proxy.get_port()), username=proxy_auth[0], password=proxy_auth[1])
            else:
                socks.set_default_proxy(socks_type, proxy.get_ip(), int(proxy.get_port()))
            socket.socket = socks.socksocket
            return True
        elif protocol == "http" or (protocol == "https" and not is_https):
            proxies = {
                "http": f"http://{proxy_auth[0]}:{proxy_auth[1]}@{proxy_address}" if proxy_auth else f"http://{proxy_address}"
            }
            session.proxies.update(proxies)
            return True
        elif protocol == "https" and is_https:
            proxies = {
                "https": f"https://{proxy_auth[0]}:{proxy_auth[1]}@{proxy_address}" if proxy_auth else f"https://{proxy_address}"
            }
            session.proxies.update(proxies)
            return True
        else:
            # Unsupported proxy protocol for the given URL
            return False

    def get_proxy(self):
        return self.proxy_pool.get_random()[0]
