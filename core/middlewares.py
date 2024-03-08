from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == '1': # Is it the HOD/Admin
                if modulename == 'core.student_views':
                    return redirect(reverse('admin_home'))
            elif user.user_type == '2': #  Staff :-/ ?
                if modulename == 'core.student_views' or modulename == 'core.hod_views':
                    return redirect(reverse('staff_home'))
            elif user.user_type == '3': # ... or Student ?
                if modulename == 'core.hod_views' or modulename == 'core.staff_views':
                    return redirect(reverse('student_home'))
            else: # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('login_page'))
        else:
            if request.path == reverse('login_page') or modulename == 'django.contrib.auth.views' or request.path == reverse('user_login'): # If the path is login or has anything to do with authentication, pass
                pass
            else:
                return redirect(reverse('login_page'))
