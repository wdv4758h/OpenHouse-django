from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

def OHlogin(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/account/login/')
        else:
            # Return an 'invalid login' error message.
            pass
    return render_to_response('login.html', context_instance=RequestContext(request))
