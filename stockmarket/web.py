# -*- coding:utf-8 -*-

def hello(request):
    from django.http import HttpResponse

    return HttpResponse("Hello world ! ")