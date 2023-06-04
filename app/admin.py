from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(user_inform)
admin.site.register(user_explain)
admin.site.register(clint_details)
admin.site.register(clint_orders)
admin.site.register(Book)