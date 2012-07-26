from django.shortcuts import render_to_response 
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Context, loader
from django.contrib.auth.decorators import login_required
from my_forms import GroupOwnershipForm
import logging

__logger__ = logging.getLogger(__name__)

@login_required
def index(request):
    #print 'request: {}'.format(str(request)) #debug
    '''the main page for this application'''
    if not request.user.has_perm('webapp.privileged'):
        return render_to_response('invalid.html')

    else:
        if not request.method == 'POST':
            group_ownership_form = GroupOwnershipForm()
            loader.get_template('index.html')
            context = Context()
            return render_to_response('index.html',
                {'group_ownership_form':group_ownership_form},
                context_instance=RequestContext(request))

        elif (u'groupname' in request.POST.keys()):
            form = GroupOwnershipForm(request.POST)
            if not form.is_valid():
                return HttpResponse("form not valid...")
            else:
                groupname = str(request.POST[u'groupname'])
                print 'groupname: ' + groupname #debug
                try:
                    #here's where the app should do its thing
                    pass
                except Exception, err:
                    __logger__.info('error: '+str(err))

                response = 'here is an http response.'

                return HttpResponse(response)
