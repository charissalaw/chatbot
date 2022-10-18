from ninja import NinjaAPI
from ninja.renderers import BaseRenderer
import json
import requests, random, re
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from chatbot.settings import (
    VERIFY_TOKEN,
    PAGE_ACCESS_TOKEN,
)

def call_send_api(sender_id, response):
    endpoint = f'https://graph.facebook.com/v15.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    response_msg = json.dumps({"recipient":{"id":sender_id}, "message":{"text":response}})
    status = requests.post(
        endpoint,
        headers = {"Content-Type": "application/json"},
        data=response_msg
    )
    print(status.json())
    return status.json()

def handle_message(sender_id, incoming_message):
    response = "no text received"
    # import pdb; pdb.set_trace()
    if incoming_message['message']['text']:
        response = "We got your message"
    call_send_api(sender_id, response)

# this is the only view not using Django-Ninja. See commented code below for detail
class FacebookWebhookView(View):
    @method_decorator(csrf_exempt) # required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) #python3.6+ syntax

    def get(self, request, *args, **kwargs):
        hub_mode   = request.GET.get('hub.mode')
        hub_token = request.GET.get('hub.verify_token')
        hub_challenge = request.GET.get('hub.challenge')
        if hub_token != VERIFY_TOKEN:
            return HttpResponse('Error, invalid token', status=403)
        return HttpResponse(hub_challenge)

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        if body['object'] == 'page':
            for entry in body['entry']:
                if entry['messaging']:
                    for message in entry['messaging']:
                        sender = message['sender']['id']
                        handle_message(sender, message)
            return HttpResponse('Event Received', status=200)
        return HttpResponse('Invalid page body', status=400)
