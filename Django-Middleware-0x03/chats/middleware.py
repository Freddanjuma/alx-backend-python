import logging
from datetime import datetime
from datetime import datetime
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store IP access data: { ip: { "count": int, "start_time": datetime } }
        self.user_messages = {}
        self.TIME_WINDOW = timedelta(minutes=1)
        self.MAX_MESSAGES = 5

    def __call__(self, request):
        user_ip = request.META.get("REMOTE_ADDR")

        # Apply rate-limiting only for POST requests (messages)
        if request.method == "POST":
            now = datetime.now()

            if user_ip not in self.user_messages:
                # First message from this IP
                self.user_messages[user_ip] = {"count": 1, "start_time": now}
            else:
                data = self.user_messages[user_ip]
                elapsed = now - data["start_time"]

                if elapsed > self.TIME_WINDOW:
                    # Reset window after 1 minute
                    self.user_messages[user_ip] = {"count": 1, "start_time": now}
                else:
                    # Count messages within the same 1-minute window
                    data["count"] += 1

                    if data["count"] > self.MAX_MESSAGES:
                        return JsonResponse(
                            {"error": "Message limit exceeded. Try again later."},
                            status=429
                        )

        return self.get_response(request)

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


class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # Only allow admins or moderators
        if user and user.is_authenticated:
            role = getattr(user, "role", None)  # assuming role is stored on the user model

            if role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Permission denied. Admin or moderator role required."},
                    status=403
                )

        return self.get_response(request)
