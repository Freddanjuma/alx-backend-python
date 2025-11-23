import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """Middleware initialization"""
        self.get_response = get_response

        # Configure logger
        logging.basicConfig(
            filename="requests.log",
            level=logging.INFO,
            format="%(message)s"
        )

    def __call__(self, request):
        """This runs for every request"""

        user = request.user if request.user.is_authenticated else "Anonymous"
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"

        logging.info(log_entry)

        response = self.get_response(request)
        return response
