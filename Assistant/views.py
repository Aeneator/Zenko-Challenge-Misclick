from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from . import gpt_funcs


def update_data(request):
    response, markers_list = gpt_funcs.answer(request.GET.get('text', None), gpt_funcs.get_client_ip(request))

    data = {"message": response,
            "markers": markers_list}
    return JsonResponse(data)


def main_page(request):
    #gpt_funcs.chat_logs[gpt_funcs.get_client_ip(request)] = []
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render())
