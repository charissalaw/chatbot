from django.contrib import admin
from django.urls import path

from chatbot.api import api
from chatbot.views.webhooks.api import FacebookWebhookView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/webhooks/webhook', FacebookWebhookView.as_view(), name='webhook'),
    path('api/', api.urls)
]
