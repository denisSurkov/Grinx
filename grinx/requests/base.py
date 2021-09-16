class BaseRequest:
    def __init__(self, method: str, request_uri: str, protocol: str):
        self.protocol: str = protocol
        self.method: str = method
        self.request_uri = request_uri

    @staticmethod
    def from_header(method: str, request_uri: str, protocol: str):
        return BaseRequest(method, request_uri, protocol)
