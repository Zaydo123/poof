import json
import useragents

class HeadersGenerator:

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        if 'file_path' in kwargs:
            self.read_headers_from_file(kwargs['file_path'])
        elif type(kwargs) == dict:
            self.headers = json.loads(kwargs)
        else:
            self.headers ={}

    def read_headers_from_file(self, file_path):
        with open(file_path, 'r') as file:
            self.headers = json.load(file)

    def get_headers(self):
        return self.headers
    
    def set(self, **kwargs):
        self.headers.update(kwargs)

    def gen_ua(self, platform=None):
        ua = useragents.UserAgent()
        if platform:
            u = ua.get_random(platform=platform)
            self.headers.update({'User-Agent': u})
        else:
            u = ua.get_random()
            self.headers.update({'User-Agent': u})
        return u
    
    def get(self, key):
        return self.headers[key]
    
    def get_all(self):
        return self.headers
    
    def get_headers(self):
        return self.headers
    