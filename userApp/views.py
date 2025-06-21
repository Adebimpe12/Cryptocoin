from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import SignUpForm, User_form, Profile_form
from django.contrib.auth.models import User
from userApp.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.contrib import messages
from django.db import transaction

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
    
@login_required
def myProfile(request, user_id):
    profile = Profile.objects.all().filter(profile_id=user_id)
    print (profile)
    return render(
        request=request,
        template_name='userApp/profile_page.html',
        context={"user_profile":profile}
    )


@login_required
def editProfile(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user_form = User_form(request.POST, instance=user)
        profile_form = Profile_form(request.POST or None, request.FILES or None, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
                if profile_form.cleaned_data['staff']:
                    user.is_staff = True
                    user.save()
                else:
                    user.is_staff = False
                    user.save()
            messages.success(request, ('Your profile was successfully updated'))
            return myProfile(request, user_id)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponsePermanentRedirect(reverse('edit_profile', args=(user_id,)))
    else:
        user_form = User_form(instance=user)
        profile_form = Profile_form(instance=user.profile)
        return render(request, 'userapp/edit_profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form
        })
    

@login_required
def deactivateProfile(request, user_id):
    print("This is to test activation")
    user = User.objects.get(id=user_id)
    if user.is_active == True:
        User.objects.filter(id=user_id).update(is_active=False)
        messages.success(request, user ('User deactivated successfully'))
    else:
        print("This is to activate")
        User.objects.filter(id=user).update(is_active=True)
        messages.success(request, user ('User activated successfully'))
    
    return HttpResponsePermanentRedirect(reverse("my_profile", args=(user_id)))
        

@login_required
def allStaff(request):
    global status
    staff = Profile.objects.all().filter(staff=True)
    status = "staff"
    return render(request, "userApp/display_all_user.html", {"allusers":staff, "status":"staff"})

@login_required
def allCustomers(request):
    global status
    customer = Profile.objects.all().filter(staff=False)
    status = "customer"
    return render(request, "userApp/display_all_user.html", {"allusers":customer, "status":"customer"})

@login_required
def deleteUser(request, user_id):
    Profile.objects.filter(user_id=user_id).delete()
    User.objects.filter(id=user_id).delete()
    if status == "staff":
        return allStaff(request)
    else:
        return allCustomers(request)