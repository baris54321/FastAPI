from fastapi import HTTPException
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def has_exception(func):
    
    @wraps(func)  # ✅ preserve FastAPI signature for dependency injection
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception("Unexpected error occurred")  # ✅ log traceback
            return {
                "data": None,
                "status": "error",
                "message": "An error occurred while processing your request.",
            }
    return wrapper
