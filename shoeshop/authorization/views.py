from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from .utils import generate_token

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.warning(request, "Passwords do not match")
            return redirect('/authorization/signup/')

        if User.objects.filter(username=email).exists():
            messages.warning(request, "User already exists")
            return redirect('/authorization/signup/')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.is_active = False  # Ensure the user is inactive until activation
        user.save()

        email_subject = "Activate Your Account"
        message = render_to_string('activation.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user),
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])

        try:
            email_message.send(fail_silently=False)  # Don't fail silently, show errors
            print("✅ Email sent successfully!")  # Debugging message
        except Exception as e:
            print(f"❌ Error sending email: {e}")  # Print error if email fails

        messages.success(request, "Account created successfully. Please check your email to activate your account.")
        return redirect('/authorization/login/')

    return render(request, 'signup.html')



class ActivateAccountview(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully')
            return redirect('/authorization/login/')
        return render(request, 'activation_failed.html')

def handlelogin(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        myuser = authenticate(username=username, password=password)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login successful")
            return redirect('/')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('/authorization/login/')

    return render(request, 'login.html')

from django.contrib.messages import get_messages

def handlelogout(request):
    storage = get_messages(request)
    for _ in storage:  
        pass

    logout(request)
    messages.info(request, "Logout successful")
    return redirect('/authorization/login/')
