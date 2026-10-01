 

from django.views.generic import DetailView
from django.http import JsonResponse
from .models import Pays, Ville


class PaysDetailView(DetailView):
    model = Pays

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())


class VilleDetailView(DetailView):
    model = Ville

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(self.object.json())