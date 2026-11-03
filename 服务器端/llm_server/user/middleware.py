import jwt
from django.conf import settings
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    """
    全局 JWT 认证中间件：
    - 放行登录/注册等白名单接口
    - 解析 Authorization: Bearer <token>
    - 将 payload 挂载到 request.user
    """

    EXEMPT_PATH_PREFIXES = (
        "/admin/",
        "/static/",
        "/user/login/",
        "/user/register/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path or ""

        if request.method == "OPTIONS" or self._is_exempt_path(path):
            return self.get_response(request)

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        token = self._extract_bearer_token(auth_header)
        if not token:
            return JsonResponse(
                {"status": "fail", "message": "缺少认证token"},
                status=401,
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {"status": "fail", "message": "token已过期"},
                status=401,
            )
        except jwt.InvalidTokenError:
            return JsonResponse(
                {"status": "fail", "message": "token无效"},
                status=401,
            )

        request.user = payload
        return self.get_response(request)

    def _is_exempt_path(self, path):
        return any(path.startswith(prefix) for prefix in self.EXEMPT_PATH_PREFIXES)

    def _extract_bearer_token(self, auth_header):
        if not auth_header:
            return ""
        if auth_header.startswith("Bearer "):
            return auth_header[7:].strip()
        return ""
