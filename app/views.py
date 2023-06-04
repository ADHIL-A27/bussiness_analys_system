from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
import textwrap
from django.http import FileResponse
from reportlab.pdfgen import canvas
import io
from datetime import date
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.core.files.storage import FileSystemStorage
from app.models import user_explain
from app.models import clint_details
from app.models import user_inform
from app.models import clint_orders
from app.models import Book
from django.shortcuts import get_object_or_404, redirect
import random
import math
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.template import loader


# Create your views here.
def index(request):
    return render(request, 'index.html')


def user(request):
    return render(request, 'about.html')


def customers(request):

    query = request.GET.get('query')
    if query:
        posts = clint_details.objects.filter(code__icontains=query)
    else:
        posts = clint_details.objects.all()

    context = {'query': query, 'posts': posts}

    # query = request.GET.get('q', '')
    # posts=clint_details.objects.annotate(search=SearchVector('name', 'description')).filter(search=query)
    # context={"posts":posts}

    return render(request, 'customers.html', context)


def analayis(request):
    query = request.GET.get('query')
    if query:
        requirs = clint_orders.objects.filter(due_date__icontains=query)
    else:
        requirs = clint_orders.objects.all()

    tests = clint_details.objects.all()
    count = clint_details.objects.count()
    latest_total_amount = clint_details.objects.latest('id')
    total_amount = latest_total_amount.total_price
    dates = [test.pub_date.strftime('%Y-%m-%d %H:%M:%S') for test in tests]

    context = {
        'count': count,
        'total_amount': total_amount,
        'tests': tests,
        'dates': dates,
        'requirs': requirs,
    }

    order_id = request.POST.get('order_id')
    if order_id:
        order = get_object_or_404(clint_orders, pk=order_id)
        order.delete()
        return redirect('analayis')

    return render(request, 'analayis.html', context)


def generate(request):

    if request.method == "POST":

        get_name = request.POST.get('clint_name')
        get_email = request.POST.get('clint_email')
        get_phone = request.POST.get('clint_phone')
        digits = "A1B2C3D4E5F6G7H8I9"
        CODE = ""
        for i in range(5):
            CODE += digits[math.floor(random.random() * 10)]
        get_code = CODE
        get_desc = request.POST.get('desc')
        get_amount = int(request.POST.get('amount'))
        latest_total_price = clint_details.objects.latest('id')
        get_total = int(latest_total_price.total_price)+(get_amount)
        query = clint_details(clint_name=get_name, clint_email=get_email, clint_phone=get_phone, code=get_code,
                              price=get_amount, total_price=get_total, desc=get_desc)
        query.save()

    return render(request, 'generate.html')


def orders(request):

    if request.method == "POST":

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        content = request.POST.get('content')
        date = request.POST.get('date')
        query = clint_orders(name=name, phone=phone,
                             content=content, due_date=date)
        query.save()

    return render(request, 'order.html')


def generate_pdf(request):

    if 'image1' not in request.FILES:
        # Handle the error or set a default image path
        filepath = 'static/bg.jpg'
    else:
        # Process the uploaded image file
        image = request.FILES['image1']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        # Get the file path
        filepath = os.path.join(fs.location, filename)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionalit

    p.drawImage(filepath, x=0, y=0,
                width=p._pagesize[0], height=p._pagesize[1], preserveAspectRatio=True)

    current_date = date.today().strftime('%B %d, %Y')
    p.setFont('Helvetica-Bold', 12)
    p.drawString(400, 700, f"{current_date}")

    p.setFont("Helvetica-Bold", 36)
    latest_user_title = user_explain.objects.latest('id')
    title = latest_user_title.title
    title_width = p.stringWidth(title, "Helvetica-Bold", 36)
    p.drawString((p._pagesize[0] - title_width) / 2, 750, title)

    p.setFont("Helvetica-Bold", 10)
    latest_user_about = user_explain.objects.latest('id')
    about = latest_user_about.about_bill
    about_width = p.stringWidth(about, "Helvetica-Bold", 10)
    p.drawString((p._pagesize[0] - about_width) / 2, 738, about)

    p.setFont("Helvetica-Bold", 10)
    latest_user_verified = user_explain.objects.latest('id')
    verified = latest_user_verified.verified
    verified_width = p.stringWidth(verified, "Helvetica-Bold", 10)
    p.drawString((p._pagesize[0] - verified_width) / 2, 726, verified)

    p.setFont("Helvetica-Bold", 17)
    latest_clint_code = clint_details.objects.latest('id')
    info_id = "IFD:"+latest_clint_code.code
    info_id_width = p.stringWidth(info_id, "Helvetica-Bold", 17)
    p.drawString((p._pagesize[0] - info_id_width) / 2, 705, info_id)

    p.setFont("Helvetica", 20)
    latest_clint_name = clint_details.objects.latest('id')
    name = 'Helloo   ' + latest_clint_name.clint_name
    name_width = p.stringWidth(name, "Helvetica-Bold", 17)
    p.drawString((p._pagesize[0] - name_width) / 8, 660, name)

    p.setFont("Helvetica", 18)
    latest_user_content = user_explain.objects.latest('id')
    text = latest_user_content.content
    lines = textwrap.wrap(text, width=50)
    y = 620
    for line in lines:
        p.drawString(100, y, line)
        y -= 20
    latest_user_name = user_inform.objects.latest('id')
    fuck = latest_user_name.user_name
    p.setFont('Helvetica', 15)
    p.drawString(100, 350, f"{fuck}")

    latest_user_email = user_inform.objects.latest('id')
    mango = latest_user_email.user_email
    p.setFont('Helvetica', 15)
    p.drawString(50, 20, f"{mango}")

    latest_user_phone = user_inform.objects.latest('id')
    phonenumber = latest_user_phone.user_phone
    p.setFont('Helvetica', 15)
    p.drawString(370, 20, f"{phonenumber}")

    if 'image2' not in request.FILES:
        # Handle the error or set a default image path
        sign = 'static/sign.jpg'
    else:
        # Process the uploaded image file
        image = request.FILES['image2']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        # Get the file path
        sign = os.path.join(fs.location, filename)

    x = 1 * inch
    y = 1 * inch
    width = 2 * inch
    height = 1 * inch

    # Load the image and draw it on the PDF
    p.drawImage(sign, x, y, width, height, preserveAspectRatio=True)

    if 'image3' not in request.FILES:
        # Handle the error or set a default image path
        seal = 'static/seal.jpg'
    else:
        # Process the uploaded image file
        image = request.FILES['image3']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        # Get the file path
        seal = os.path.join(fs.location, filename)

    x = 5 * inch
    y = 1 * inch
    width = 2 * inch
    height = 1 * inch

    # Load the image and draw it on the PDF
    p.drawImage(seal, x, y, width, height, preserveAspectRatio=True)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    pdf_bytes = buffer.getvalue()

    latest_clint_email = clint_details.objects.latest('id')

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = 'a8727449@gmail.com'
    msg['To'] = latest_clint_email.clint_email
    msg['Subject'] = '(BFCS) CARD FROM HOOCX'

    body = 'hello '+latest_clint_name.clint_name + \
        'i attached a pdf in this email ,first of all i request to you please read that completely, if you \seem any problem in my product or service mustely i want this pdf other wise i not accept it '
    msg.attach(MIMEText(body))

# Attach the PDF file from the variable
    attach = MIMEApplication(pdf_bytes, _subtype='pdf')
    attach.add_header('Content-Disposition', 'attachment',
                      filename=latest_user_title.title+'.pdf')
    msg.attach(attach)

# Send the email
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    username = 'a8727449@gmail.com'
    password = 'jqnp nzye ntdw doai'
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    server.sendmail(username, msg['To'], msg.as_string())
    server.quit()

    # Get the value of the BytesIO buffer and return the PDF as a response.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=latest_user_title.title+'.pdf')


def inker(request):
    if request.method == "POST":

        get_title = request.POST.get('title')
        get_verified = request.POST.get('Verified')
        get_about_bill = request.POST.get('about_bill')
        get_content = request.POST.get('content')
        query = user_explain(title=get_title, verified=get_verified,
                             about_bill=get_about_bill, content=get_content)
        query.save()
    return render(request, 'work.html')


# printa
