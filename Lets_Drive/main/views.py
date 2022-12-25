from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import *
from .forms import UsersForm
import hashlib


# Create your views here.


def index(request):
    autos = []
    for auto in Auto.objects.order_by('id'):
        if auto.available:
            autos.append(auto)
    if 'login' in request.session:
        return render(request, "main/index.html", {'autos': autos, 'login': request.session['login']})
    else:
        return render(request, "main/index.html", {'autos': autos, 'login': False})


def signin(request):
    if 'login' in request.session:
        return index(request)
    else:
        return render(request, "main/signin.html")


def signup(request):
    if request.method == 'POST':
        fio = request.POST['fio']
        photo_pass = request.FILES['photo_pass']
        photo_vu = request.FILES['photo_vu']
        md5 = hashlib.md5(b'59283')
        password = request.POST['password']
        md5.update(password.encode('utf-8'))
        password = md5.hexdigest()
        form = Users(fio=fio, password=password, photo_pass=photo_pass, photo_vu=photo_vu, age=0, staz=0,
                     available=False)
        form.save()
        return signin(request)
    if 'login' in request.session:
        return index(request)
    else:
        return render(request, "main/signup.html", {'form': UsersForm()})


def profile(request):
    drives = Drives.objects.order_by('-time_start')
    if request.method == 'POST':
        drive1 = Drives()
        for drive in drives:
            if str(drive) == request.POST['drive']:
                drive1 = drive
        photo = request.FILES['photo']
        status = "на рассмотрении"
        form = Breaks(drive=drive1, photo=photo, status=status)
        form.save()
        return index(request)
    users = Users.objects.order_by('id')
    drive_list = []
    breaks_list = []
    breaks = Breaks.objects.order_by('id')
    for user in users:
        if 'login' in request.session and user.fio == request.session['login']:
            if 'login' in request.session:
                for drive in drives:
                    if drive.user_id == user.id:
                        drive_list.append(drive)
                for break_ in breaks:
                    if break_.drive.user_id == user.id:
                        breaks_list.append(break_)
                return render(request, "main/profile.html",
                              {'login': request.session['login'], 'user': user, 'drives': drive_list,
                               'breaks': breaks_list})
    return signin(request)


def car(request):
    tarify = Tarify.objects.order_by('id')
    autos = Auto.objects.order_by('id')
    for auto in autos:
        if auto.id == int(request.COOKIES.get('index')):
            if 'login' in request.session:
                return render(request, "main/car.html",
                              {'auto': auto, 'x': request.COOKIES.get('x'), 'y': request.COOKIES.get('y'),
                               'tarify': tarify, 'login': request.session['login']})
            else:
                return render(request, "main/car.html",
                              {'auto': auto, 'x': request.COOKIES.get('x'), 'y': request.COOKIES.get('y'),
                               'tarify': tarify, 'login': False})
    return index(request)


@csrf_protect
def send_coord(request):
    response = render(request, "main/car.html")
    if request.method == "POST":
        response.set_cookie('x', request.POST.get('x'))
        response.set_cookie('y', request.POST.get('y'))
        response.set_cookie('index', int(request.POST.get('index')))
    return response


@csrf_protect
def auth_session(request):
    if request.method == "POST":
        users = Users.objects.order_by('id')
        for user in users:
            if user.fio == request.POST.get('login'):
                if not user.available:
                    return JsonResponse({'error': 'error-available'})
                md5 = hashlib.md5(b'59283')
                password = request.POST.get('password')
                md5.update(password.encode('utf-8'))
                password = md5.hexdigest()
                if user.password == password:
                    request.session['login'] = request.POST.get('login')
                    return render(request, "main/profile.html")
                return JsonResponse({"error": "error-pass"})
        return JsonResponse({"error": "error-login"})
    return signin(request)


@csrf_protect
def exit_user(request):
    if request.method == "POST":
        del request.session['login']
        return index(request)
    return signin(request)


@csrf_protect
def check_form(request):
    if request.method == "POST":
        if request.POST.get('fio').isalpha():
            users = Users.objects.order_by('id')
            for user in users:
                if user.fio == request.POST.get('fio'):
                    return JsonResponse({"error": 'error-name-exists'})
            if len(request.POST.get('password')) < 8:
                return JsonResponse({"error": 'error-pass'})
            if request.POST.get('password') != request.POST.get('confirm_password'):
                return JsonResponse({"error": 'error-pass2'})
        else:
            return JsonResponse({"error": 'error-name'})
    return JsonResponse({"error": 'none'})


@csrf_protect
def selecttarif(request):
    if request.method == "POST":
        tarify = Tarify.objects.order_by('id')
        for tarif in tarify:
            if tarif.id == int(request.POST.get("tarif")) and tarif.available:
                return JsonResponse(
                    {"time": tarif.time_limit, "distance": tarif.distance_limit, "pr_km": tarif.price_km,
                     "pr_m": tarif.price_minute, "pr": tarif.price})
    return JsonResponse({"error": 'error'})


@csrf_protect
def registerdrive(request):
    if request.method == "POST":
        users = Users.objects.order_by('id')
        for user in users:
            if 'login' not in request.session:
                return JsonResponse({"error": 'login'})
            if user.fio == request.session['login']:
                autos = Auto.objects.order_by('id')
                for auto in autos:
                    if auto.id == int(request.POST.get("auto_id")):
                        form = Drives(auto=auto, user=user, distance=request.POST.get("distance"),
                                      time_start=request.POST.get("time_start"),
                                      time_finish=request.POST.get("time_finish"), price=request.POST.get("price"))
                        form.save()
                        return JsonResponse({"success": 'success'})
    return JsonResponse({"error": 'error'})
