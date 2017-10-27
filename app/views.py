from django.shortcuts import render, HttpResponse, redirect
from app import models
from django import views
from django.utils.decorators import method_decorator


def outer(func):
    def inner(req, *args, **kwargs):
        print(req.method)
        return func(req, *args, **kwargs)

    return inner


@method_decorator(outer, name="dispatch")  # 最终方案
class Login(views.View):
    def get(self, req, *args, **kwargs):
        return render(req, 'login.html')

    def post(self, req, *args, **kwargs):
        username = req.POST.get("username", None)
        password = req.POST.get("password", None)
        c = models.Administrator.objects.filter(username=username, password=password).count()
        if c:
            # rep.set_cookie('username', username) 不加密
            req.session['username'] = username
            return redirect("/index")
        else:
            return render(req, "login.html", {"notice": "用户名密码错误"})


def logout(request):
    request.session.clear()
    return redirect('/login')


def auth(func):
    def inner(request, *args, **kwargs):
        is_login = request.session.get('username')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect('/login')

    return inner


@auth
def index(request):
    session = request.session.get('username')
    return render(request, 'index.html', {'username': session, 'title': ' 首页'})


@method_decorator(auth, name="dispatch")
class HandleClasses(views.View):
    def get(self, request, *args, **kwargs):
        current_user = request.session.get('username')
        classes = models.Classes.objects.all()
        return render(request, 'classes.html', {'username': current_user, 'classes': classes})

    def post(self, request, *args, **kwargs):
        import json
        response_dict = {'status': True, 'error': None, 'data': None}
        caption = request.POST.get('caption', None)
        if caption:
            models.Classes.objects.create(caption=caption)
        else:
            response_dict['status'] = False
            response_dict['error'] = '内容不能为空'
        return HttpResponse(json.dumps(response_dict),content_type="application/json")


@auth
def handle_student(request):
    current_user = request.session.get('username')
    return render(request, 'student.html', {'username': current_user})


@auth
def handle_teacher(request):
    current_user = request.session.get('username')
    return render(request, 'teacher.html', {'username': current_user})
