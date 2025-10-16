import logging
import time
from fastapi import Request

class LoggingMiddleware:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    async def __call__(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        self.logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.2f}s"
        )

        response.headers["X-Process-Time"] = str(process_time)
        return response