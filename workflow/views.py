from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from user.models import Profile
from .models import *
from .serializers import *

class WorkflowView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        workflows = Workflow.objects.filter(owner = self.request.user) | Workflow.objects.filter(users__id__exact=self.request.user.id)
        serializer = WorkflowSerializer(workflows, many=True)
        return Response({"workflows": serializer.data})


@login_required
def workflows(request):
    return render(request, 'workflows/main.html')


@login_required
def workflow(request, workflow_id):

    try:
        workflow = Workflow.objects.get(id=workflow_id)
    except Workflow.DoesNotExist:
        raise Http404
    
    if workflow.owner != request.user and request.user not in workflow.users:
        raise Http404
    
    # TODO: Fix havy DB load code
    accept_user_profile = []

    for user in workflow.users.all():
        accept_user_profile.append(Profile.objects.get(user=user))

    render_context = {
        'workflow': workflow,
        'accept_user_profile': accept_user_profile
    }

    return render(request, 'workflows/single.html', render_context)