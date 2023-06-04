from django.db import models


class user_inform(models.Model):
    user_name=models.CharField(max_length=100)
    user_phone=models.CharField(max_length=15)
    user_email=models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

class user_explain(models.Model):
    title = models.CharField(max_length=100)
    verified=models.CharField(max_length=100)
    about_bill=models.CharField(max_length=100)
    content = models.TextField()

class clint_details(models.Model):
    clint_name=models.CharField(max_length=100)
    code=models.CharField(max_length=50)
    price=models.CharField(max_length=50)
    clint_phone=models.CharField(max_length=15)
    clint_email=models.CharField(max_length=100)
    total_price=models.CharField(max_length=50)
    desc=models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)

class clint_orders(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    content = models.TextField()
    due_date=models.CharField(max_length=50)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    publication_date = models.DateField()

    def __str__(self):
        return self.title



    