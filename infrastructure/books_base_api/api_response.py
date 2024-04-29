class ApiResponse:
    def __init__(self, status: int, result):
        self.status = status
        self.result = result
