import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Restrict access outside 6AM (6) to 9PM (21)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Chat access is allowed only between 6AM and 9PM.")

        # Continue normal processing
        response = self.get_response(request)
        return response

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = getattr(request, 'user', 'Anonymous')
        log_message = f"{datetime.now()} - User: {user} - Path: {getattr(request, 'path', '')}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response
