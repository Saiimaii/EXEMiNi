from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
import json
from datetime import datetime, timedelta



# Create your views here.
def index(request):
    return render(request, "index.html")

def signup(request):
    return render(request, "signup.html")

def login(request):
    return render(request, "login.html")

def addUser(request):
    username = request.POST['username']
    firstname = request.POST['firstname']
    email = request.POST['email']
    password = request.POST['password']
    repassword = request.POST['repassword']
    
    if password==repassword:
        if User.objects.filter(username=username).exists():
            #print("Username นี้ซ้ำ")
            return redirect('/signup/')
        elif User.objects.filter(email=email).exists():
            #print("email นี้ซ้ำ")
            return redirect('/signup/')
        else:
            user = User.objects.create_user(
                username = username,
                first_name = firstname,
                email = email,
                password = password
            )
            user.save()
            return redirect('/')
    else:
        #print("password ไม่ตรงกัน repassword")
        return render(request,"signup.html")
    
def loginFrom(request):
    username = request.POST['username']
    password = request.POST['password']
    
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        #แสดง  U&P ถูกต้อง
        auth.login(request,user)
        return redirect('/backend/')
    else:
        #แสดง  U&P ไม่ถูกต้อง
        return redirect('/login/')

def change(request, id):
    try:
        user = User.objects.get(id=id)  
    except User.DoesNotExist:
        messages.error(request, "ไม่พบผู้ใช้นี้") 
        return redirect('change')  

    if request.method == "POST":
        user.username = request.POST["username"]
        user.first_name = request.POST["firstname"]
        user.email = request.POST["email"]
        user.save() 
        messages.success(request, "บันทึกข้อมูลเรียบร้อยแล้ว")
        return redirect('about')
    
    return render(request, "change.html", {"user": user})

def backend(request):
    return render(request, "backend.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def porder(request):
    return render(request, "porder.html")

from .models import Datashop

def new(request):
    if request.method == 'POST':
        date = request.POST['date']  
        num = request.POST['num']
        order = request.POST['order']
        product = request.POST['product']
        quantity = request.POST['quantity']
        totalPrece = request.POST['totalPrece']
        address = request.POST['address']
        message = request.POST['message']

        # ดึงข้อมูล user
        user = User.objects.get(username=request.user.username)

        # สร้างออเดอร์ใหม่
        datashop = Datashop.objects.create(
            user=user,
            datesend=date,
            num_order=num,
            order=order,
            product=product,
            quantity=quantity,
            totalPrece=totalPrece,
            address=address,
            message=message,
        )
        
        return redirect('/myorder/')
    else:
        return render(request, "porder.html")
    

def myorder(request):
    all_dataorder = Datashop.objects.filter(user=request.user)
    return render(request,"myorder.html",{"all_dataorder":all_dataorder})

def delete(request,datashop_id):
    dataorder = Datashop.objects.get(id=datashop_id)
    dataorder.delete()
    return redirect("/myorder/")

def edit(request,datashop_id):
    if request.method == "POST":
        dataorder = Datashop.objects.get(id=datashop_id)
        dataorder.address = request.POST["address"]
        dataorder.message = request.POST["message"]
        dataorder.save()
        return redirect("/myorder/")
    else:
        dataorder = Datashop.objects.get(id=datashop_id)
        return render(request, "edit.html",{"dataorder":dataorder})
    
def contact(request):
    return render(request, "contact.html")

def about(request):
    user = request.user  
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'email': user.email,
        'password': user.password,
        # ไม่ควรแสดง password
    }
    return render(request, 'about.html', context)


@login_required
def change_password(request, id):
    user = User.objects.get(id=id) 
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # อัปเดตเซสชัน
            return redirect('about')  
    else:
        form = PasswordChangeForm(user)

    return render(request, 'change_password.html', {'form': form})

def all_order(request):
    all_order = Datashop.objects.all()
    return render(request, 'all_order.html', {'all_order': all_order})

def update_status(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('payment_status_'):
                order_id = key.split('_')[2] 
                try:
                    order = Datashop.objects.get(id=order_id)
                    order.payments_status = value
                    order.save()
                except Datashop.DoesNotExist:
                    return HttpResponse("Order not found.")

            elif key.startswith('product_status_'):
                order_id = key.split('_')[2]
                try:
                    order = Datashop.objects.get(id=order_id)
                    order.products_status = value
                    order.save()
                except Datashop.DoesNotExist:
                    return HttpResponse("Order not found.")

        return redirect('/all_order/')

    all_orders = Datashop.objects.all() 
    return render(request, 'all_order.html', {'all_order': all_orders})


@staff_member_required
def list_name(request):
    all_list = User.objects.all()
    return render(request, "list_name.html", {"all_list": all_list})


def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("/all_user/")

def edit_user(request, id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        user.username = request.POST["username"]
        user.first_name = request.POST["first_name"]
        user.email = request.POST["email"]
        user.last_login = request.POST["last_login"]
        user.save()
        return redirect("/all_user/")
    else:   
        user = User.objects.get(id=id)
        return render(request, "all_user.html",{"user": user})
    
def weekly_product_data(request):
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # วันจันทร์ของสัปดาห์นี้

    # กำหนดรูปแบบข้อมูลที่จะส่งกลับ
    data = {
        "labels": ['จันทร์', 'อังคาร', 'พุธ', 'พฤหัสบดี', 'ศุกร์', 'เสาร์', 'อาทิตย์'],
        "data": [0] * 7  # จำนวนวันในสัปดาห์ (0-6)
    }

    # ใช้ฟิลด์ datesend แทน date
    products = Datashop.objects.filter(datesend__gte=start_of_week, datesend__lt=start_of_week + timedelta(days=7)).values('datesend').annotate(count=Count('id'))

    for product in products:
        day_of_week = product['datesend'].weekday()  # 0 = จันทร์, 1 = อังคาร, ..., 6 = อาทิตย์
        data['data'][day_of_week] += product['count']  # เพิ่มจำนวนสินค้าในวันนั้น

    return JsonResponse(data)

def chart_view(request):
    return render(request, 'chart_view.html')