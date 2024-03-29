from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from APPS.accounts.models import Account, Profile
from .forms import RegistrationForm, ProfileForm, AccountForm

from django.core.mail import EmailMessage

from APPS.orders.models import Order, OrderProduct

from APPS.cart.services import get_cart_id
from APPS.cart.models import Cart, CartItem


from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.decorators import login_required

def registerPage(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
                
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password )

                
            if phone_number != '' :
                user.phone_number = phone_number
            user.save()

            # Create user profile
            profile = Profile.objects.create(user=user)
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Welcome to my Shopango!'
            message = render_to_string('accounts/verification_email.html', {
                'user':user,
                'domain': current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            # messages.success(request, 'We have send verification email to you. Please verify it.')
            return redirect('/account/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()


    context = {"form":form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        print(request.user)
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = Account.objects.get(email=email)
        except:
            messages.error(request, "Account with email does not exist!")
        
        # try:
        #     user = Account.objects.get(email=email, password=password)
        # except:
        #     messages.error(request, "Password is 4 wrong!")

        user = authenticate(request, email=email, password=password) 

        if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=get_cart_id(request))
                    does_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    
                    if does_cart_item_exists:
                        cart_items = CartItem.objects.filter(cart=cart)
                        product_variations = []

                        for item in cart_items:
                            variation = item.variations.all()
                            product_variations.append(list(variation))


                        cart_item = CartItem.objects.filter(user=user)
                        created_variation_list = []
                        id = []
                        for item in cart_item:
                            created_variation = item.variations.all()
                            created_variation_list.append(list(created_variation))
                            id.append(item.id)
                        
                        for option in product_variations:
                            if option in created_variation_list:
                                index = created_variation_list.index(option)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()

                except:
                    pass
                
                login(request, user)
                return redirect(request.POST.get('next') if 'next' in request.POST else 'dashboard')
                # if 'next' in request.POST:
                #     return redirect(request.POST.get('next'))
                # else:
                #     return redirect('dashboard')

                # nie działalo 
                #  return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            pass   
                    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    messages.info(request, "Logout succesfully!")
    return redirect("login")

# def activate(request, uidb64, token):
#     return HttpResponse('Activation succesfull!')

def activate(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated successfully! Now you can sign in')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link. Something is not yes')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    user = request.user
    # print(f'This is user id: {user}')
    orders = Order.objects.filter(user_id=user.id, is_ordered = True)
    orders_count = orders.count()
    context = {'user':user, 'orders':orders, 'orders_count':orders_count}
    return render(request, 'accounts/dashboard.html', context)


def resetPassword(request):
    if request.method == 'POST':
        email = request.POST['email'].lower()

        if Account.objects.filter(email__exact=email).exists():
            # Reset password email
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain': current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Passwort reset email has been send.')
            return redirect('login')
        else:
            messages.error(request, 'Account with this email does not exist!')
            return redirect('resetpassword')

    return render(request, 'accounts/resetpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        # uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
        
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset password')
        return redirect('new_password')
    else:
        messages.error(request, 'This link is no longer active!')
        return redirect('login')
    

def new_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        uid = request.session.get('uid')

        if uid != None:
            if password == confirm_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful!')
                return redirect('login')
            
            else:
                messages.error(request, 'Passwords do note match!')
                return redirect('new_password')
        else:
            return redirect('login')
    return render(request, 'accounts/new_password.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered = True).order_by('-created_at')
    context = {
        'orders':orders
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
def eddit_profile(request):
    userprofile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        user_form = AccountForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profiles has been updated')
            return redirect('eddit_profile')
    else:
        user_form = AccountForm(instance=request.user)
        profile_form= ProfileForm(instance=userprofile)

    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
    }
    return render(request, 'accounts/eddit_profile.html', context)

@login_required(login_url='login')
def eddit_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(email__exact=request.user.email)
        if new_password ==  confirm_new_password:
            succes = user.check_password(current_password)
            if succes:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password updated successfully")
                return redirect('eddit_password')
            else:
                messages.error(request, "Please enter valid password")
                return redirect('eddit_password')
        else:
            messages.error(request, "Password does not match")
            return redirect('eddit_password')
    context = {}
    return render(request, 'accounts/eddit_password.html', context)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
        }
    return render(request, 'accounts/order_detail.html', context)




