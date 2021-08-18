from django.db import models
import re
from datetime import datetime


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if (len(postData['registered_first_name']) == 0 or
            len(postData['registered_last_name']) == 0 or
            len(postData['registered_email']) == 0 or
            len(postData['registered_password']) == 0 or
            len(postData['registered_address']) == 0 or
            len(postData['registered_city']) == 0 or
            len(postData['registered_state']) == 0 or
                len(postData['registered_zipcode']) == 0):
            errors['empty_field'] = "All fields must be completed for registration."

        if len(postData['registered_first_name']) < 2:
            errors['first_name_error'] = 'The first name has to be at least 2 characters.'
        if len(postData['registered_last_name']) < 2:
            errors['last_name_error'] = 'The last name has to be at least 2 characters.'
        if len(postData['registered_address']) < 2:
            errors['address_error'] = 'Your address has to be at least 2 characters.'
        if len(postData['registered_city']) < 2:
            errors['city_error'] = 'The city must have at least 2 characters.'
        if len(postData['registered_state']) < 2:
            errors['state_error'] = 'Please use a 2 letter state code'
        if len(postData['registered_zipcode']) != 5:
            errors['zipcode_error'] = 'Please use a 5 digit zipcode'
        if not EMAIL_REGEX.match(postData['registered_email']):
            errors['email'] = "Invalid email address!"
        if postData['registered_password'] != postData['registered_confirm_pw']:
            errors['password_no_match'] = 'Your passwords do not match.'
        if len(postData['registered_password']) < 8:
            errors['short_password'] = 'The password has to be at least 8 characters.'
        return errors


class AdminManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['admin_email']):
            errors['email'] = "Invalid email address!"
        if len(postData['admin_password']) < 8:
            errors['short_password'] = 'The password has to be at least 8 characters.'

        return errors


class ProductInfo(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.DecimalField(decimal_places=2, max_digits=5)
    item_description = models.TextField(max_length=255)
    store_count = models.IntegerField(default=0)
    cart_count = models.IntegerField(default=0)
    item_size = models.CharField(max_length=5)
    #cart = models.ManyToManyField('Cart', related_name = "selected_items")
    # product_image = ImageField(upload_to=get_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sandal(ProductInfo):
    pass


class Clog(ProductInfo):
    pass


class WaterFriendly(ProductInfo):
    pass


class Cart(models.Model):
    #selected_items (Many_to_Many)
    cart = models.ForeignKey(
        'User', related_name="user_cart", on_delete=models.CASCADE)
    order_processing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #item_quantity_in_cart = models.IntegerField(max=99)


class User(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_2 = models.CharField(default='', max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #user_cart (One_to_Many)


class Admin(models.Model):
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AdminManager()
