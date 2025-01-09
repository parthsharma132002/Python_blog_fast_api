from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, conint, constr
from typing import Any

class SuccessResponseSerializer(BaseModel):
    status: conint() = status.HTTP_200_OK
    message: constr() = "Success"
    data: Any = None
    
class ErrorResponseSerializer(BaseModel):
    status: conint() = status.HTTP_400_BAD_REQUEST
    message: constr() = "error"
    data: Any = None
    
