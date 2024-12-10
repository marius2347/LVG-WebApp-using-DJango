from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import email_change_token 
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from .models import Product
from .models import Profile
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


# Create your views here.
def home(request):
    return render(request, 'home.html')

def features(request):
    return render(request, 'features.html')

def shop(request):
    return render(request, 'shop.html')

def template(request):
    return render(request, 'template.html')


def lvg_collection(request):
    return render(request, 'lvg_collection.html')

def lvgdesign_collection(request):
    return render(request, 'lvgdesign_collection.html')

def lvgwear_collection(request):
    return render(request, 'lvgwear_collection.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def support(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose the email content
        email_subject = f"Support Request: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        # Send the email
        try:
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['mariusc0023@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent! We will get back to you shortly.')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}. Please try again later.")

        return redirect('support')
    
    return render(request, 'support.html')

# def register(request):
#     if request.method == 'POST':
#         name = request.POST['name']  # This is the full name (first + last)
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
        
#         if password == confirm_password:
#             if User.objects.filter(username=email).exists():
#                 messages.error(request, "Email already taken.")
#             else:
#                 # Split the name into first and last names
#                 first_name, last_name = (name.split(' ', 1) + [""])[:2]  # Split full name into first and last name parts

#                 user = User.objects.create_user(
#                     username=email, 
#                     password=password, 
#                     email=email, 
#                     first_name=first_name,
#                     last_name=last_name
#                 )
#                 user.save()
#                 messages.success(request, "Account created successfully. Please log in.")
#                 return redirect('login')
#         else:
#             messages.error(request, "Passwords do not match.")
    
#     return render(request, 'register.html')

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, MinimumLengthValidator, CommonPasswordValidator, NumericPasswordValidator
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

def register(request):
    errors = {}  # Dictionary to store field-specific errors
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Validate form fields
        if not name:
            errors['name'] = ["Full name is required."]
        else:
            first_name, last_name = (name.split(' ', 1) + [""])[:2]  # Split full name into first and last name

        if not email:
            errors['email'] = ["Email is required."]
        elif User.objects.filter(username=email).exists():
            errors['email'] = ["Email already taken."]
        
        if not password:
            errors['password'] = ["Password is required."]
        elif password != confirm_password:
            errors['confirm_password'] = ["Passwords do not match."]
        else:
            # Run Django's built-in password validators
            try:
                validate_password(password, user=None, password_validators=[
                    MinimumLengthValidator(),
                    CommonPasswordValidator(),
                    NumericPasswordValidator()
                ])
            except ValidationError as e:
                errors['password'] = list(e.messages)  # Store password validation errors

        if not errors:  # If no errors, proceed with account creation
            user = User.objects.create_user(
                username=email, 
                password=password, 
                email=email, 
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")

    return render(request, 'register.html', {'errors': errors})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate user based on email and password
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Invalid email or password.")
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')



User = get_user_model()

# @login_required
# def profile(request):
#     password_form = PasswordChangeForm(request.user, request.POST or None)

#     if request.method == 'POST':
#         if 'change_password' in request.POST:
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)  # Keep the user logged in after the password change
#                 messages.success(request, 'Password changed successfully.')
#                 return redirect('profile')
#             else:
#                 messages.error(request, 'Please correct the errors below.')

#     return render(request, 'profile.html', {
#         'password_form': password_form,
#     })

@login_required
def profile(request):
    password_form = PasswordChangeForm(request.user, request.POST or None)

    # Retrieve or create a Profile instance
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keep the user logged in after password change
                messages.success(request, 'Password changed successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')

    return render(request, 'profile.html', {
        'password_form': password_form,
        'profile': profile,
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Get the current user
        user = request.user

        # Update full name only if provided
        if full_name:
            first_name, last_name = (full_name.split(' ', 1) + [""])[:2]
            user.first_name = first_name
            user.last_name = last_name

        # Update email only if provided
        if email:
            user.email = email

        user.save()

        # Handle profile image upload
        profile, created = Profile.objects.get_or_create(user=user)
        if 'profile_image' in request.FILES:
            profile.image = request.FILES['profile_image']
            profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return redirect('profile')

# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('full_name', '').strip()
#         email = request.POST.get('email', '').strip()

#         # Split the full name into first and last name parts
#         first_name, last_name = (full_name.split(' ', 1) + [""])[:2]

#         user = request.user
#         user.first_name = first_name
#         user.last_name = last_name
#         if email:
#             user.email = email
#         user.save()
#         messages.success(request, 'Profile updated successfully.')
#         return redirect('profile')

#     return redirect('profile')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            # Render profile page with form errors
            return render(request, 'profile.html', {'form': form})

    # If method is GET, redirect to profile as no separate template is required
    return redirect('profile')

@login_required
def support_profile(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_name = request.user.get_full_name() or request.user.username
        user_email = request.user.email

        # Compose the full message
        full_message = f"From: {user_name} <{user_email}>\n\nMessage:\n{message}"

        try:
            # Send email
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,  
                recipient_list=[settings.EMAIL_HOST_USER],  
                fail_silently=False,
            )
            messages.success(request, 'Support message sent successfully.')
        except Exception as e:
            messages.error(request, f"An error occurred while sending the email: {e}. Please try again later.")

    return redirect('profile')

@login_required
def request_email_change(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        if new_email:
            current_site = get_current_site(request)
            mail_subject = f'Confirm your email change on {current_site.name}'
            uid = urlsafe_base64_encode(force_bytes(request.user.pk))
            token = email_change_token.make_token(request.user)

            # Create the confirmation link with new_email as a query parameter
            confirmation_link = f"{request.build_absolute_uri(reverse('confirm_email_change', kwargs={'uidb64': uid, 'token': token}))}?new_email={new_email}"

            # Render email content from template
            html_message = render_to_string('email_change_confirmation_email.html', {
                'user': request.user,
                'confirmation_link': confirmation_link,
                'current_site': current_site,
            })
            
            # Prepare and send the email
            email = EmailMultiAlternatives(
                subject=mail_subject,
                from_email='no-reply@example.com',
                to=[request.user.email]
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            messages.success(request, 'A confirmation email has been sent to your actual address.')
            return redirect('profile')
    return redirect('profile')





User = get_user_model()

# def confirm_email_change(request, uidb64, token):
#     new_email = request.GET.get('new_email')  # Retrieve the new email from query parameters

#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and email_change_token.check_token(user, token) and new_email:
#         user.email = new_email
#         user.save()
#         messages.success(request, 'Your email has been updated successfully.')
#         return redirect('profile')
#     else:
#         messages.error(request, 'The email change link is invalid or has expired.')
#         return redirect('profile')


def confirm_email_change(request, uidb64, token):
    new_email = request.GET.get('new_email')  # Retrieve the new email from query parameters

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_change_token.check_token(user, token) and new_email:
        user.email = new_email
        user.username = new_email  # Update the username to match the new email
        user.save()
        messages.success(request, 'Your email has been updated successfully.')
        return redirect('profile')
    else:
        messages.error(request, 'The email change link is invalid or has expired.')
        return redirect('profile')


def send_password_reset_email(request, email):
    try:
        # Look up the user by email
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return False

    # Generate the password reset token and URL
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = request.build_absolute_uri(
        reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    )

    # Get the current site name and domain for the email template
    current_site = get_current_site(request)
    
    # Render the HTML email content from the template
    email_subject = 'Reset Your Password'
    html_message = render_to_string('reset_password_email.html', {
        'reset_link': reset_link,
        'current_site': current_site,
    })

    # Use EmailMultiAlternatives to send the HTML email
    email = EmailMultiAlternatives(
        subject=email_subject,
        body="Please use the link below to reset your password.",
        from_email=settings.EMAIL_HOST_USER,
        to=[email]
    )
    email.attach_alternative(html_message, "text/html")
    email.send()

    return True



# Define the password reset request view
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if send_password_reset_email(request, email):
            messages.success(request, 'Your password has been reseted. Now login!')
            return redirect('password_reset_done')
        else:
            messages.error(request, 'Email address not found.')
            return redirect('password_reset')
    return render(request, 'forgot_password.html')


def search(request):
    query = request.GET.get('query', '').lower()

    # Define the redirect map
    redirects = {
        'features': '/features/',
        'features.html': '/features/',
        'lvg collection': '/lvg-collection/',
        'lvg': '/lvg-collection/',
        'lvg_collection.html': '/lvg-collection/',
        'lvg wear': '/lvgwear-collection/',
        'wear': '/lvgwear-collection/',
        'lvgwear_collection.html': '/lvgwear-collection/',
        'lvg design': '/lvgdesign-collection/',
        'design': '/lvgdesign-collection/',
        'lvgdesign_collection.html': '/lvgdesign-collection/',
        'support': '/support/',
        'support.html': '/support/',
    }

    # Check if the query matches any redirects
    if query in redirects:
        return JsonResponse({'status': 'success', 'redirect': redirects[query]})
    else:
        return JsonResponse({'status': 'error', 'message': 'Page not found!'})


