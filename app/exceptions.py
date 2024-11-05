from fastapi.exceptions import HTTPException
from requests.exceptions import RequestException


class DetailNotFound(HTTPException):
    def __init__(self, model_name):
        super(DetailNotFound, self).__init__(status_code=404, detail=f"{model_name} not found")


class NBPAPIError(RequestException):
    def __init__(self, model_name):
        super(NBPAPIError, self).__init__(status_code=404, detail=f"{model_name} not found")
