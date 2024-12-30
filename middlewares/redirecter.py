from django.urls import resolve, Resolver404
from django.http import HttpResponseRedirect
from loguru import logger

class Redirecter():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            path = request.path
            resolve(path)
        except (Resolver404, Exception, ) as e:
            # logger.error(
            #     str(e)
            # )

            return HttpResponseRedirect('/chat/')
        
        return self.get_response(request)
