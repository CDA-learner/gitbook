# ~*~ coding: utf-8 ~*~

from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
import os,sys,re,time
from common.utils import get_logger
from django.contrib.auth.decorators import login_required

@login_required
def MapIndexVies(TemplateView):
    template_name = "map.html"

    return render(TemplateView, template_name)

@login_required
def MapRenderIndexVies(TemplateView):
    template_name = "map_render.html"

    return render(TemplateView, template_name)

def MapView(request):
    os.system('python /opt/jumpserver/apps/accessmap/creatmap.py')
    time.sleep(10)
    receipt = json.dumps({"status": 0, "info": request.GET})
    return HttpResponse(receipt)






