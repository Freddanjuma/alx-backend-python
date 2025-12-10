from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

@csrf_exempt
def delete_user(request):
    """
    Simple delete_user endpoint:
    - Expects POST with username + password
    - Authenticates the user
    - Deletes the user instance
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    username = request.POST.get("username")
    password = request.POST.get("password")

    if not username or not password:
        return JsonResponse({"error": "username and password required"}, status=400)

    user = authenticate(username=username, password=password)
    if not user:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    user.delete()  # This will trigger the post_delete signal
    return JsonResponse({"message": "User account deleted successfully"})
