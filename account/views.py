from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm,UpdateProfileForm#, AccountUpdateForm
from .models import Account

# Create your views here.
def index(request):
    return render(request,'account/home.html')


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('index')
        else:
            context['registration_form'] = form

    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')



def login_view(request):
    context={}

    user=request.user
    if user.is_authenticated:
        return redirect('index')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("index")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "account/login.html", context)



#TODO this is not correct method
"""
@login_required
def update_profile(request):
    account=Account.objects.get(email=request.user.email)
    if request.method == 'POST':
        edit_form=UpdateProfileForm(request.POST or None,request.FILES or None,instance=account)
        if edit_form.is_valid():
            acc_profile=edit_form.save(commit=False)
            acc_profile.save()
            account=acc_profile
            messages.success(request,f"Your Profile is updated successfully{account.email}")
            return redirect('profile')
        else:
            messages.warning(request,"Something Went Wrong..!")
            return redirect('profile')
    form=UpdateProfileForm(
        initial={
            "email":account.email,
            "username":account.username,
            "phone_number":account.phone_number,
        }
    )
    context={
        'form':form,
        # 'account':account,
    }
    return render(request,'account/profile_edit.html',context)
"""

@login_required
def update_profile(request):
    """
    context={

    }
    if request.method == 'POST':
        edit_form=UpdateProfileForm(request.POST ,instance=request.user)
        if edit_form.is_valid():
            edit_form.initial={
                "email":request.POST['email'],
                "username":request.POST['username'],
            }
            edit_form.save()
            context['success_message'] = "Updated"
            messages.success(request,"Your Profile is updated successfully")
            # return redirect('profile')
        else:
            messages.warning(request,"Something Went Wrong..!")
            # return redirect('profile')
    else:
        edit_form=UpdateProfileForm(
            initial={
                "email":request.user.email,
                "username":request.user.username,
                "phone_number":request.user.phone_number,
            }
            )

    context['account_form']=edit_form,
    """

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
                "phone_number": request.POST['phone_number'],
            }
            form.save()
            messages.success(request, "Your Profile is updated successfully")
            context['success_message'] = "Updated"
    else:
        form = UpdateProfileForm(
            initial={  # TODO:  is user for initial value already filled in the form
                "email": request.user.email,
                "username": request.user.username,
                "phone_number": request.user.phone_number,

            }
        )

    context['form'] = form

    return render(request,'account/profile_edit.html',context)