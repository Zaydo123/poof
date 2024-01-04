class HeadersGenerator:

    # Incomplete for now

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.headers ={
        }

    def generate_headers(self):
        headers = {}
        for key, value in self.kwargs.items():
            headers[key] = value
        return headers
        