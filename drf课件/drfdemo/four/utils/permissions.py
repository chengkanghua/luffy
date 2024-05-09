from rest_framework.permissions import BasePermission


class IsXiaoMingPermission(BasePermission):
    def has_permission(self, request, view):
        print(request)
        print(view)
        if (request.user.username == "xiaoming"):
            return True