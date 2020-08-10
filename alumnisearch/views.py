# django imports 
from random import randint
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password, make_password
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage
from django.db import transaction
from django.views.generic import View

#project imports
from .models import *
from .utils import *
from .constants import *
from .forms import RegistrationForm, SignInForm, ProfileForm, UserForm, ChangePasswordForm
from alumni_network import settings



class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'

    """API View for the dashboard view for the user"""
    def get(self, request):
        return render(request,'home.html')    


class UserSignUp(View):
    """API View for signing up a user after filling the registration form"""

    def get(self,request):
        form = RegistrationForm() 
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            next_url = self.request.POST.get('next')
            success_url = reverse('login')
            if next_url:
                success_url += '?next={}'.format(next_url)
            return redirect(success_url)
        else:
            messages.warning(request, 'Please fill the mandatory fields correctly!')    
        return render(request, 'registration/register.html', {'form': form})


class UserSignIn(View):
    """API View for logging in a user with the required credentials."""

    def get(self,request):
        form = SignInForm() 
        return render(request,template_name = "registration/login.html", context={"form":form})

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {user.full_name}")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'registration/login.html')
        return redirect(reverse('home'))


class ProfileView(LoginRequiredMixin, View):
    """API View for showing the profile of the user."""

    def get(self, request):
        form = ProfileForm(request.user)
        return render(request,template_name = "registration/profile.html", context={"form":form})


class ProfileUpdateView(LoginRequiredMixin, View):
    """API View for updating the profile of the user."""

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict() or None
        file_data = request.FILES or None
        try:
            with transaction.atomic():
                user_profile, created = AlumnusProfile.objects.get_or_create(alumnus=request.user)
                user_qs = User.objects.filter(pk=request.user.pk).values().first()
                user_profile_qs = AlumnusProfile.objects.filter(pk=user_profile.pk).values().first()
                user_form = UserForm(post_data, file_data, instance=request.user)
                profile_form = ProfileForm(post_data, instance=user_profile)
                for index, val in request.POST.items():
                    if index in USER_FORM_KEYS:
                        post_data[index] = user_qs.get(index) if not post_data.get(index) else val
                    else:
                        post_data[index] = user_profile_qs.get(index) if not post_data.get(index).strip() else post_data[index]
                if user_form.is_valid():
                    user_form.save()
                if profile_form.is_valid() and user_form.is_valid():
                    profile_form.save()
                    messages.success(request, 'Your profile is updated successfully!')
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    messages.error(request, "Please fill the form correctly!")
        except ValueError as error:
            messages.error(request, str(error))
        except Exception as e:
            messages.error(request, INVALID_DATE_MESG) if user_form.errors.get("dob") else messages.error(request, GENERIC_ERR)
        return render(request, 'registration/profile-update.html', context={"profile_form":profile_form, 'user_form':user_form})    

    def get(self, request):
        profile_form = ProfileForm(request.user)
        user_form = UserForm(request.user)
        return render(request, template_name = "registration/profile-update.html", context={"profile_form":profile_form, 'user_form':user_form})


class ChangePassword(LoginRequiredMixin, View):
    """API View for changing the password of the user."""

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict() or None
        if not request.user.check_password(post_data.get("old_password")):
            messages.error(request, "The old password is incorrect!")
        change_password_form = ChangePasswordForm(post_data)
        with transaction.atomic():
            if change_password_form.is_valid():
                new_password = change_password_form.data.get("new_password")
                request.user.password = make_password(new_password)
                request.user.save()
                return redirect(reverse('home'))
            else:
                messages.error(request, "passwords don't match or some other error with form!")
        return render(request, 'registration/change_password.html', context={"password_form":change_password_form})

    def get(self, request, *args, **kwargs):
        change_password_form = ChangePasswordForm()
        return render(request, template_name = "registration/change_password.html", context={"password_form":change_password_form})


class ForgotPassword(View):
    """API View for sending the password of the user via mail if password is forgotten."""
    def post(self, request, *args, **kwargs):
        try:
            post_data = request.POST.dict() or None
            user_data = User.objects.filter(email = post_data.get("email"))
            if not user_data.exists() :
                messages.error(request, "This email is not registered with the user!") 
            else:
                user = user_data.first()      
                new_password = randint(100000, 999999)
                email_id = post_data.get("email")
                subject = "Forgot Password Mail"
                context = {'name': user.full_name, 'new_password': new_password}
                recipient = [email_id]
                FROM = SENDGRID_SENDER
                body = "Password reset"
                msg_html = render_to_string('registration/password_mail.html', context)
                status = send_email(subject, body, FROM, recipient, msg_html)
                if status:
                    messages.info(request, "Your new password has been sent to your email id!")
                    user.password = make_password(new_password)
                    user.save()
                else:
                    messages.info(request, "Connection error, mail can't be sent!")
        except Exception as e:
            messages.info(request, GENERIC_ERR)
        return render(request, 'registration/forgot_password.html')

    def get(self, request, *args, **kwargs):
        return render(request, template_name = "registration/forgot_password.html")

class ListAlumni(LoginRequiredMixin, View):
    """API View for listing all the alumni on the basis of name/batch year as typed by the logged in user."""

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('-created_at').exclude(pk=self.request.user.uuid)

    def filter_queryset(self, params, queryset):
        from django.db.models import Q
        if params.get("name") and not params.get("batch_year"):
            return queryset.filter(Q(full_name__icontains=params.get("name").strip(), city__icontains=self.request.user.city, \
                school__icontains=self.request.user.school))
        if params.get("batch_year") and not params.get("name"):
            return queryset.filter(Q(batch_year=params.get("batch_year").strip(), city__iexact=self.request.user.city, \
                school__icontains=self.request.user.school))
        else:
            return queryset.filter(batch_year=params.get("batch_year").strip(), full_name__icontains = \
                params.get("name").strip(), city__iexact=self.request.user.city, school__icontains=self.request.user.school)

    def get(self, request, *args, **kwargs):
        try:
            params = request.GET.dict()
            filtered_qs = self.filter_queryset(params, self.get_queryset())
            pagenumber = request.GET.get('page', 1)
            paginator = Paginator(filtered_qs, 10)
            res_user_data = list(paginator.page(pagenumber).object_list.values())   
            users = paginate(res_user_data, paginator, pagenumber)
            users = paginator.get_page(pagenumber)
            return render(request,  'alumni_list.html', {'users': users, 'params':params})      
        except Exception as e:
            messages.info(request, GENERIC_ERR)
        return render(request, 'home.html')

class ProfileRetrieve(LoginRequiredMixin, View):
    """API View for view all the details of the desired alumnus."""

    def get(self, request, id):
        try:
            if not User.objects.filter(pk=id).exists():
                messages.error(request, GENERIC_ERR)
            user_data = User.objects.filter(pk=id).values().first()
            profile= AlumnusProfile.objects.select_related("user").filter(alumnus_id=id). \
                            values('description','website_url','dob').first()
            profile_data = profile if profile else {}
            user_data.update(profile_data)
        except Exception:
            messages.error(request, GENERIC_ERR)
        return render(request, 'show_alumni_det.html', context={"profile":user_data})

