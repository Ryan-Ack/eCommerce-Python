from django.urls import path
from . import views

urlpatterns = [
    # Render User Paths*****************************************
    path('', views.category),
    path('carts', views.carts),
    path('show/<int:item_id>', views.show),
    path('loginandreg', views.loginandreg),

    # Render Admin Paths*********************************
    path('admin', views.admin),
    path('dashboard/orders', views.admin_orders),
    path('dashboard/products', views.admin_products),
    path('dashboard/product/create', views.product_create),
    path('dashboard/product/edit/<int:product_id>', views.product_edit),
    path('admin/dash/show', views.admin_dash_show),

    # Redirect Admin Paths*********************************
    path('dashboard/product/process_create', views.product_process_create),
    path('dashboard/product/process_edit/<int:product_id>', views.product_process_edit),
    path('dashboard/product/delete/<int:product_id>', views.product_delete),
    path('admin_logout', views.admin_logout),
    path('admin_login', views.admin_login),

    # Redirect User Paths**********************************
    path('logout', views.logout),
    path('user_login', views.user_login),
    path('user_register', views.user_register),
    path('addtocart', views.addtocart),
]
