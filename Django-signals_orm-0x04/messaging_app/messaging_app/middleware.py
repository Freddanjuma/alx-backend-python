from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware to log each user's request with timestamp, username, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get username if authenticated, else "Anonymous"
        user = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else "Anonymous"

        # Log the request
        with open("request_logs.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        # Continue processing the request
        response = self.get_response(request)
        return response
