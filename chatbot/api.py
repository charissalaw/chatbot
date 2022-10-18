from ninja import NinjaAPI, Schema, Form
from ninja.renderers import BaseRenderer

from store.api import router as store_router


api = NinjaAPI()
api.add_router("/store", store_router)
