from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Clog, WaterFriendly, Sandal, User, ProductInfo, Admin
from datetime import datetime
import bcrypt

# Render Page Functions****************************


def registration(request):
    return render(request, 'registration.html')


def category(request):
    # Paginator
    sandal_list = Sandal.objects.get_queryset().order_by('id')
    paginator = Paginator(sandal_list, 2)
    page = request.GET.get('page', 1)
    try:
        sandals = paginator.page(page)
    except PageNotAnInteger:
        sandals = paginator.page(1)
    except EmptyPage:
        sandals = paginator.page(paginator.num_pages)
    # End Paginator
    context = {
        'sandals': sandals,
        'all_sandals': len(sandal_list),
        'total_products': len(ProductInfo.objects.all()),
        'page': page,
        'all_clogs': len(Clog.objects.all()),
        'all_waterfriendlys': len(WaterFriendly.objects.all()),
    }
    return render(request, 'category.html', context)


def carts(request):
    # user_cart = User.objects.get(id=request.post(["user_id"]))

    # context = {
    #     # "user": User.objects.last()
    #     "user": User.objects.get(id=request.session['user_id']),
    #     "user_cart": Cart.objects.all(),
    #     "product_info": ProductInfo.objects.all(),
    #     "cart_length": Cart.objects.all()('cart.user_cart.all | length'),
    #     # .order_by('thought.users_who_liked.all | length')
    # }
    # context = {
    #     'sandals': sandals,
    #     'all_sandals': len(sandal_list),
    #     'total_products': len(ProductInfo.objects.all()),
    #     'page': page,
    #     'all_clogs': len(Clog.objects.all()),
    #     'all_waterfriendlys': len(WaterFriendly.objects.all()),
    # }

    return render(request, 'carts.html')


def addtocart(request):

    return redirect('/show')


def show(request, item_id):
    item = Sandal.objects.get(id=item_id)
    price = item.item_price
    context = {
        'items': item,
        'price_list': {'1': price, '2': price*2, '3': price*3},
        'all_products': ProductInfo.objects.all(),
    }
    print(context)
    return render(request, 'show.html', context)
# would it be item_in_cart_id??


def deleteitem(request, cart_id):
    print(request.POST)
    deletethisitem = Cart.objects.get(id=cart_id)
    deletethisitem.delete()
    return redirect('/carts')


def loginandreg(request):
    return render(request, 'loginandreg.html')

# Render admin  Functions**************************


def admin_login(request):
    all_errors = Admin.objects.validator(request.POST)

    if len(all_errors) > 0:
        for key, val in all_errors.items():
            messages.error(request, val)
        return redirect('/admin')
    admin_list = Admin.objects.filter(email=request.POST['admin_email'])
    if len(admin_list) == 0:
        messages.error(request, "Please check your email/password")
        messages.error(request, "Are you looking for the user login?")
        return redirect("/admin")

    # request.session['admin_id'] = admin_list[0].id
    return redirect('/dashboard/orders')


def admin(request):
    return render(request, 'adminlogin.html')


def admin_logout(request):
    request.session.flush()
    return redirect("/admin")


def admin_dash_show(request):
    return render(request, 'adminDashShow.html')


def admin_orders(request):
    return render(request, 'adminorders.html')


def admin_products(request):
    all_products = ProductInfo.objects.all()
    context = {
        'all_products': all_products,
    }
    return render(request, 'adminproducts.html', context)


def product_create(request):
    return render(request, 'productcreate.html')

def product_edit(request, product_id):
    context = {
        'product_to_edit': ProductInfo.objects.get(id=product_id),
    }
    return render(request, 'productedit.html', context)

# Redirect Admin  Functions**************************


def product_process_create(request):
    print(request.POST)
    if "cancel" in request.POST:
        return redirect('/dashboard/products')
    if request.POST['category'] == 'Sandal':
        print('created sandal')
        Sandal.objects.create(
            item_name=request.POST['item_name'],
            item_price=request.POST['item_price'],
            item_description=request.POST['item_description'],
            item_size=request.POST['item_size']
        )
    if request.POST['category'] == 'Clog':
        print('created clog')
        Clog.objects.create(
            item_name=request.POST['item_name'],
            item_price=request.POST['item_price'],
            item_description=request.POST['item_description'],
            item_size=request.POST['item_size']
        )
    if request.POST['category'] == 'WaterFriendly':
        print('created waterfriendly')
        WaterFriendly.objects.create(
            item_name=request.POST['item_name'],
            item_price=request.POST['item_price'],
            item_description=request.POST['item_description'],
            item_size=request.POST['item_size']
        )
    return redirect('/dashboard/products')

def product_process_edit(request, product_id):
    print('edited sandal')
    product = ProductInfo.objects.get(id=product_id)
    product.item_name = request.POST['item_name']
    product.item_price = request.POST['item_price']
    product.item_description = request.POST['item_description']
    product.item_size = request.POST['item_size']
    product.save()
    print(product.item_name, product.item_description)
    return redirect('/dashboard/products')

def product_delete(request, product_id):
    product = ProductInfo.objects.get(id=product_id)
    product.delete()
    return redirect('/dashboard/products')
# Redirect User Functions**************************


def user_login(request):
    user_list = User.objects.filter(email=request.POST['login_email'])
    # user_list = User.objects.get(email=request.POST['login_email'])
    if len(user_list) == 0:
        messages.error(request, "Please check your email/password")
        messages.error(request, "Do you need to register?")
        return redirect("/loginandreg")

    if not bcrypt.checkpw(request.POST['login_password'].encode(), user_list[0].password.encode()):
        messages.error(request, "Please check your email/password")
        return redirect("/loginandreg")

    request.session['user_id'] = user_list[0].id
    #
    return redirect('/')


def user_register(request):
    errors = User.objects.validator(request.POST)

    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/loginandreg')

    password = request.POST['registered_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    created_user = User.objects.create(
        first_name=request.POST['registered_first_name'],
        last_name=request.POST['registered_last_name'],
        email=request.POST['registered_email'],
        password=pw_hash,
        address=request.POST['registered_address'],
        city=request.POST['registered_city'],
        state=request.POST['registered_state'],
        zipcode=request.POST['registered_zipcode'],
    )
    request.session['user_id'] = created_user.id

    # request.session['user_id'] = created_user.id
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect("/")
