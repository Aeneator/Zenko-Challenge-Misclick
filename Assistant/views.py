from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from . import gpt_funcs


def update_data(request):
    response = gpt_funcs.ask_question_topic(request.GET.get('text', None), gpt_funcs.get_client_ip(request))

    data = {"message": response}
    return JsonResponse(data)


def main_page(request):
    gpt_funcs.chat_logs[gpt_funcs.get_client_ip(request)] = []
    template = loader.get_template('main_page.html')
    return HttpResponse(template.render())
