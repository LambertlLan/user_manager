from django.shortcuts import render, HttpResponse, redirect
from app import models
from django import views
from django.utils.decorators import method_decorator


def outer(func):
    def inner(req, *args, **kwargs):
        print(req.method)
        return func(req, *args, **kwargs)

    return inner


class Login(views.View):
    # def dispatch(self, request, *args, **kwargs):
    #     print(111)
    #     # 此处get,post方法还没执行
    #     # 调用父类中的dispatch方法用于分发到方法函数
    #     ret = super(Login, self).dispatch(request, *args, **kwargs)
    #     # 此处get,post方法已执行完
    #     print(222)
    #     return ret

    def get(self, req, *args, **kwargs):
        return render(req, 'login.html')

    # 使用django的method_decorator方法调用装饰器
    # @method_decorator(outer)
    def post(self, req, *args, **kwargs):
        username = req.POST.get("username", None)
        password = req.POST.get("password", None)
        c = models.Administrator.objects.filter(username=username, password=password).count()
        if c:
            rep = redirect("/index")
            # rep.set_cookie('username', username) 不加密
            rep.set_signed_cookie('username', username)
            return rep
        else:
            return render(req, "login.html", {"notice": "用户名密码错误"})


# Create your views here.
# def login(req):
#     if req.method == "POST":
#         username = req.POST.get("username", None)
#         password = req.POST.get("password", None)
#         c = models.Administrator.objects.filter(username=username, password=password).count()
#         if c:
#             rep = redirect("/index")
#             # rep.set_cookie('username', username) 不加密
#             rep.set_signed_cookie('username', username)
#             return rep
#         else:
#             return render(req, "login.html", {"notice": "用户名密码错误"})
#     else:
#         return render(req, 'login.html')



def logout(request):
    request.session.clear()
    return redirect('/login')


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('is_login')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')

    return inner


# @auth
def index(request):
    current_user = request.session.get('username')
    return render(request, 'index.html', {'username': current_user})


@auth
def handle_classes(request):
    current_user = request.session.get('username')
    return render(request, 'classes.html', {'username': current_user})


@auth
def handle_student(request):
    current_user = request.session.get('username')
    return render(request, 'student.html', {'username': current_user})


@auth
def handle_teacher(request):
    current_user = request.session.get('username')
    return render(request, 'teacher.html', {'username': current_user})
