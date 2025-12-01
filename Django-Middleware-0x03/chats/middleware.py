import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
import os


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs every request to chats/requests.log
    """

    def process_request(self, request):
        # Record request start time
        request.start_time = time.time()

    def process_response(self, request, response):
        try:
            # Calculate request duration
            duration = time.time() - request.start_time
            duration = round(duration, 4)

            # Construct log entry
            timestamp = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            method = request.method
            path = request.path
            status = response.status_code

            log_entry = f"[{timestamp}] {method} {path} {status} {duration}s\n"

            # Log file path
            log_dir = os.path.join(os.path.dirname(__file__), "requests.log")

            # Write to requests.log
            with open(log_dir, "a") as log_file:
                log_file.write(log_entry)

        except Exception as e:
            pass  # Ensures middleware never breaks the app

        return response
