class BaseCallRailException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.kwargs = kwargs
        self.printed_message = self.message

        if "status_code" in self.kwargs:
            self.status_code = self.kwargs["status_code"]
            self.printed_message += f" Status code: {self.status_code}"
        elif "headers" in self.kwargs:
            self.headers = self.kwargs["headers"]
            self.printed_message += f" Headers: {self.headers}"
        elif "response" in self.kwargs:
            self.response = self.kwargs["response"]
            self.printed_message += f" Response: {self.response}"

        super().__init__(self.printed_message)
