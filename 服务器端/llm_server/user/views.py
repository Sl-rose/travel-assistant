from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import hashlib
import jwt
import datetime
import uuid
import os
from functools import wraps
from django.conf import settings
# Create your views here.
# 密码加密函数
def hash_password(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest()
def generate_token(user):
    """生成 JWT token"""
    payload = {
        'userid': user.id,
        'name': user.name,
        'phone': user.phone,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=settings.JWT_EXPIRE_DAYS),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token

def verify_token(token):
    """验证 JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(view_func):
    """token 验证装饰器"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # 从 header 中获取 token
        token = request.META.get('HTTP_AUTHORIZATION', '')
        if token.startswith('Bearer '):
            token = token[7:]
        
        # 如果 header 中没有，尝试从参数中获取
        if not token:
            token = request.GET.get('token', '') or request.POST.get('token', '')
        
        if not token:
            return JsonResponse({"status": "fail", "message": "缺少认证token"}, status=401)
        
        # 验证 token
        payload = verify_token(token)
        if payload is None:
            return JsonResponse({"status": "fail", "message": "token无效或已过期"}, status=401)
        
        # 将用户信息附加到 request 对象
        request.user = payload
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@csrf_exempt
def register(request):
    """用户注册"""
    from .models import UserInfo
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        nickname = request.POST.get('nickname', '').strip()
        
        print(f"[注册] 收到请求 - username: {username}, nickname: {nickname}")
        
        # 验证必填字段
        if not username or not password:
            return JsonResponse({"status": "fail", "message": "用户名和密码不能为空"})
        
        # 验证密码长度
        if len(password) < 6:
            return JsonResponse({"status": "fail", "message": "密码长度不能少于6位"})
        
        # 验证手机号格式
        import re
        phone_pattern = r'^1[3-9]\d{9}$'
        if not re.match(phone_pattern, username):
            return JsonResponse({"status": "fail", "message": "请输入正确的手机号"})
        
        # 检查用户名是否已存在
        if UserInfo.objects.filter(phone=username).exists():
            print(f"[注册] 手机号已存在: {username}")
            return JsonResponse({"status": "fail", "message": "该手机号已注册"})
        
        # 创建新用户
        try:
            encrypted_pwd = hash_password(password)
            print(f"[注册] 准备创建用户 - name: {nickname or username}, phone: {username}")
            
            user = UserInfo.objects.create(
                name=nickname or username,
                passwd=encrypted_pwd,
                phone=username
            )
            print(f"[注册] 用户创建成功 - userid: {user.id}")
            
            # 构建用户基本信息字典
            user_info = {
                'userid': user.id,
                'name': user.name,
                'phone': user.phone,
                'avatar': user.avatar or '',
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else '',
            }
            
            return JsonResponse({
                "status": "success",
                "message": "注册成功",
                "user_info": user_info
            })
        except Exception as e:
            print(f"[注册] 错误: {str(e)}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "fail", "message": f"注册失败：{str(e)}"})
    
    return JsonResponse({"status": "fail", "message": "请求方法错误"})

@csrf_exempt
def login(request):
    """用户登录"""
    from .models import UserInfo
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        print(f"[登录] 收到请求 - username: {username}")
        
        # 验证必填字段
        if not username or not password:
            return JsonResponse({"status": "fail", "message": "用户名和密码不能为空"})
        
        # 查找用户（支持手机号或用户名登录）
        try:
            # 先尝试用手机号查找
            print(f"[登录] 尝试用手机号查找: {username}")
            user = UserInfo.objects.get(phone=username)
            print(f"[登录] 找到用户 - id: {user.id}, name: {user.name}")
        except UserInfo.DoesNotExist:
            # 再用用户名查找
            print(f"[登录] 手机号未找到，尝试用用户名查找: {username}")
            try:
                user = UserInfo.objects.get(name=username)
                print(f"[登录] 找到用户 - id: {user.id}, phone: {user.phone}")
            except UserInfo.DoesNotExist:
                print(f"[登录] 用户不存在: {username}")
                return JsonResponse({"status": "fail", "message": "用户不存在"})
        except Exception as e:
            # 捕获其他数据库错误
            print(f"[登录] 查询错误: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "fail", "message": f"服务器错误：{str(e)}"})
        
        # 验证密码
        try:
            encrypted_password = hash_password(password)
            print(f"[登录] 密码对比 - 输入密码MD5: {encrypted_password[:10]}..., 数据库MD5: {user.passwd[:10]}...")
            
            if user.passwd != encrypted_password:
                print(f"[登录] 密码错误")
                return JsonResponse({"status": "fail", "message": "密码错误"})
            
            print(f"[登录] 密码验证成功")
        except Exception as e:
            print(f"[登录] 密码验证错误: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({"status": "fail", "message": f"密码验证失败：{str(e)}"})
        
        # 登录成功
        # 登录成功
        print(f"[登录] 登录成功 - userid: {user.id}")
        
        # 构建用户基本信息字典
        user_info = {
            'userid': user.id,
            'name': user.name,
            'phone': user.phone,
            'avatar': user.avatar or '',
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else '',
            'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S') if user.updated_at else '',
        }
        
        # 生成 JWT token
        token = generate_token(user)
        
        print(f"[登录] 用户信息: {user_info}")
        print(f"[登录] 生成token: {token[:30]}...")
        
        return JsonResponse({
            "status": "success",
            "message": "登录成功",
            "token": token,
            "user_info": user_info
        })
    
    return JsonResponse({"status": "fail", "message": "请求方法错误"})

# 示例：需要 token 验证的接口
@csrf_exempt
@token_required
def get_user_profile(request):
    """获取用户信息（需要 token 验证）"""
    if request.method == 'GET':
        # request.user 包含 token 解析后的用户信息
        userid = request.user['userid']
        
        from .models import UserInfo
        try:
            user = UserInfo.objects.get(id=userid)
            user_info = {
                'userid': user.id,
                'name': user.name,
                'phone': user.phone,
                'avatar': user.avatar or '',
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            return JsonResponse({
                "status": "success",
                "user_info": user_info
            })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                "status": "fail",
                "message": "用户不存在"
            })
    
    return JsonResponse({"status": "fail", "message": "请求方法错误"})

@csrf_exempt
@token_required
def update_user_profile(request):
    """更新用户信息（需要 token 验证）"""
    if request.method == 'POST':
        userid = request.user['userid']
        
        from .models import UserInfo
        try:
            user = UserInfo.objects.get(id=userid)
            
            # 支持 JSON 和 form-data 两种格式
            import json
            if request.content_type and 'application/json' in request.content_type:
                data = json.loads(request.body)
                name = data.get('name', '').strip()
                avatar = data.get('avatar', '').strip()
            else:
                name = request.POST.get('name', '').strip()
                avatar = request.POST.get('avatar', '').strip()
            
            if name:
                user.name = name
            if avatar:
                user.avatar = avatar
            
            user.save()
            
            return JsonResponse({
                "status": "success",
                "message": "更新成功"
            })
        except UserInfo.DoesNotExist:
            return JsonResponse({
                "status": "fail",
                "message": "用户不存在"
            })
        except Exception as e:
            return JsonResponse({
                "status": "fail",
                "message": f"更新失败：{str(e)}"
            })
    
    return JsonResponse({"status": "fail", "message": "请求方法错误"})

@csrf_exempt
@token_required
def upload_avatar(request):
    """上传用户头像（需要 token 验证）"""
    if request.method == 'POST':
        userid = request.user['userid']
        
        # 获取上传的文件
        if 'file1' not in request.FILES:
            return JsonResponse({"status": "fail", "message": "未接收到文件"})
        
        file = request.FILES['file1']
        
        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if file.content_type not in allowed_types:
            return JsonResponse({"status": "fail", "message": "只支持图片文件"})
        
        # 验证文件大小（限制为5MB）
        if file.size > 5 * 1024 * 1024:
            return JsonResponse({"status": "fail", "message": "图片大小不能超过5MB"})
        
        try:
            # 获取文件的后缀名
            ext = os.path.splitext(file.name)[1]
            
            # 生成唯一的文件名
            unique_name = f"avatar_{userid}_{uuid.uuid4().hex}{ext}"
            
            # 保存到 avatar 文件夹
            fs = FileSystemStorage(
                location=str(settings.BASE_DIR / "static" / "avatar"),
                base_url=settings.STATIC_URL + "avatar/"
            )
            
            # 保存文件
            filename = fs.save(unique_name, file)
            file_url = fs.url(filename)
            
            # 更新数据库中的头像字段
            from .models import UserInfo
            user = UserInfo.objects.get(id=userid)
            user.avatar = file_url
            user.save()
            
            return JsonResponse({
                "status": "success",
                "message": "头像上传成功",
                "file_url": file_url
            })
            
        except Exception as e:
            return JsonResponse({
                "status": "fail",
                "message": f"上传失败：{str(e)}"
            })
    
    return JsonResponse({"status": "fail", "message": "请求方法错误"})