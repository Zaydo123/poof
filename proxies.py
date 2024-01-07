from request import RequestSender
import requests
import random
import time
import threading
import queue


class ProxyTester:
    def __init__(self, proxies, thread_count=1):
        self.proxies = proxies
        self.thread_count = min(thread_count, len(proxies))

        self.proxy_queue = queue.Queue()
        for proxy in proxies:
            self.proxy_queue.put(proxy)

        self.threads = []
        self.successful_results = ProxyPool()
        self.failed_results = ProxyPool()

    def test(self, proxy):
        try:
            protocol = proxy.get_protocol()
            if(protocol == "http"):
                url = "http://httpbin.org/ip"
            else:
                url = "https://httpbin.org/ip"

            start = time.time()
            response = RequestSender(proxy_pool=ProxyPool()).send_get_request(url, custom_proxy=proxy)
            end = time.time()

            delay = end - start
            delay_to_ms = delay * 1000
            proxy.set_speed(delay_to_ms)


            if response.json()["origin"] == proxy.get_ip():
                self.successful_results.add(proxy)
                proxy.set_status("up")
            else:
                self.failed_results.add(proxy)
                proxy.set_status("insecure")


        except requests.exceptions.ProxyError:
            self.failed_results.add(proxy)
            proxy.set_status("down")


        except Exception as e:
            self.failed_results.add(proxy)
            proxy.set_status("down")


    def worker(self):
        while not self.proxy_queue.empty():
            proxy = self.proxy_queue.get()
            if proxy.get_status() is None or proxy.get_status() == "testing":
                proxy.set_status("testing")
                self.test(proxy)
            self.proxy_queue.task_done()

    def start(self):
        for i in range(self.thread_count):
            t = threading.Thread(target=self.worker)
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

    def get_successful_results(self):
        return self.successful_results
    
    def get_failed_results(self):
        return self.failed_results
    
    def get_results(self):
        return self.successful_results, self.failed_results

    def get_proxies(self):
        return self.proxies


class Proxy:
    def __init__(self, ip, port, username=None, password=None, protocol="http", speed_ms=None, status=None):
        self.protocol = protocol
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.speed_ms = None
        self.status = None

    def get_protocol(self):
        return self.protocol
    
    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
    
    def get_auth(self):
        if self.username is None or self.password is None:
            return None
        return (self.username, self.password)
    
    def get_speed(self):
        return self.speed_ms
    
    def get_status(self):
        return self.status
    
    def set_protocol(self, protocol):
        self.protocol = protocol

    def set_ip(self, ip):
        self.ip = ip
    
    def set_port(self, port):
        self.port = port
    
    def set_username(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password

    def set_auth(self, username, password):
        self.username = username
        self.password = password

    def set_speed(self, speed_ms):
        self.speed_ms = speed_ms

    def set_status(self, status):
        self.status = status

    def __str__(self):
        if self.get_auth() is not None:
            return self.ip + ":" + self.port + ":" + self.username + ":" + self.password    
        return self.ip + ":" + self.port


class ProxyPool:
    def __init__(self):
        self.pool = []

    def load(self, proxies):
        self.pool.extend(proxies)
        return len(self.pool)
    
    def combine(self, pool):
        self.pool.extend(pool.get_all())
        return len(self.pool)

    def write_to_file(self, file_path):
        if(file_path[-4:] == ".csv"):
            with open(file_path, 'a') as file:
                for proxy in self.pool:
                    if proxy.get_auth() is None:
                        file.write(proxy.ip + "," + proxy.port + "\n")
                    else:
                        file.write(proxy.ip + "," + proxy.port + "," + proxy.username + "," + proxy.password + "\n")
        else:
            with open(file_path, 'w') as file:
                for proxy in self.pool:
                    file.write(str(proxy)+"\n")

    #even proxies with auth
    def parse_proxy_txt(self, file_path, protocol="http"):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if ":" in line:
                    proxy = line.strip().split(":")
                    if len(proxy) == 2:
                        self.pool.append(Proxy(proxy[0], proxy[1], protocol=protocol))
                    elif len(proxy) == 4:
                        self.pool.append(Proxy(proxy[0], proxy[1], proxy[2], proxy[3], protocol=protocol))
                else:
                    print("Invalid proxy format: " + line,"in file: " + file_path,"\nNeeds to be in format: ip:port or ip:port:username:password")

        return len(self.pool)

    def parse_proxy_csv(self, file_path, protocol="http"):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if "," in line:
                    proxy = line.strip().split(",")
                    if len(proxy) == 2:
                        self.pool.append(Proxy(proxy[0], proxy[1], protocol=protocol))
                    elif len(proxy) == 4:
                        self.pool.append(Proxy(proxy[0], proxy[1], proxy[2], proxy[3], protocol=protocol))
                else:
                    print("Invalid proxy format: " + line,"in file: " + file_path,"\nNeeds to be in format: ip:port or ip:port:username:password")

        return len(self.pool)
    
    def read_file(self, file_path, protocol="http"): #reads proxies from file
        if file_path[-4:] == ".csv":
            return self.parse_proxy_csv(file_path, protocol=protocol)
        elif file_path[-4:] == ".txt":
            return self.parse_proxy_txt(file_path, protocol=protocol)
        else:
            print("Invalid file format: " + file_path)
            return 0

    def add(self, *args): #takes any number of Proxy objects, adds all of them to pool
        for proxy in args:
            self.pool.append(proxy)


    def remove(self, *args): #takes any number of Proxy objects, removes all of them from pool
        for proxy in args:
            self.pool.remove(proxy)
    
    def get_random(self, count=1): #returns random proxy object
        return random.sample(self.pool, count)
    
    def size(self): #returns size of pool
        return len(self.pool)

    def is_empty(self): #returns true if pool is empty
        return self.size() == 0
    
    def get_all(self): #returns all proxies in pool
        return self.pool

    def get_all_as_str(self): #returns all proxies in pool as string
        string = ""
        for proxy in self.pool:
            string += str(proxy) + "\n"
        return string
    
    def is_in_pool(self, proxy): #returns true if proxy is in pool
        return proxy in self.pool
    
    def clear(self): #clears pool
        self.pool.clear()

    def __str__(self): #returns all proxies in pool as string
        return self.get_all_as_str()

class ProxyScraper:
    def __init__(self, proxy=None, timeout=10, urls=[]):
        ## scraper pool
        self.scraped_pool = ProxyPool()
        ##
        self.proxy = proxy
        self.timeout = timeout
        self.urls = urls

        if urls == []:
            self.urls = [
              "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
              "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
              "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
                "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
            ]
    
    def write_to_file(self, file_path):
        self.scraped_pool.write_to_file(file_path)        
        
    def scrape(self, url):
        try:
                temp_pool = ProxyPool()

                # make proxy object for each then load to pool
                response = requests.get(url, timeout=self.timeout)
                lines = response.text.split("\n")
                print(len(lines))
                for line in lines:
                    if(line == "" or line == "\n" or line == " "):
                        continue
                    elif ":" in line:
                        splitted = line.split(":")
                        if len(splitted) == 2:
                            temp_pool.add(Proxy(splitted[0], splitted[1]))
                        elif len(splitted) == 4:
                            temp_pool.add(Proxy(splitted[0], splitted[1], splitted[2], splitted[3]))
                    else:
                        print("format error: ->" + line)
        except Exception as e:
            print("Error: " + str(e))
            
        return temp_pool

    def scrape_all(self):
        collected = 0
        for url in self.urls:
            pool = self.scrape(url)
            self.scraped_pool.combine(pool)
            collected += pool.size()

        print("Collected " + str(collected) + " proxies in total")
        print("Confirmed " + str(self.scraped_pool.size()) + " proxies")

        self.scraped_pool = pool
        return self.scraped_pool

    def get_pool(self):
        return self.scraped_pool

if __name__ == "__main__":
    #-- Scrape 
    scraper = ProxyScraper()
    scraper.scrape_all().write_to_file("./proxies.txt")

    #-- convert txt to csv
    #pool = ProxyPool()
    #print(pool.parse_proxy_txt("./proxies.txt"))
    #pool.write_to_file("./proxies.csv")

    #-- test proxies
    pool = ProxyPool()
    pool.read_file("./proxies.txt", protocol="http")
    tester = ProxyTester(pool.get_all(), thread_count=50)
    tester.start()


    



