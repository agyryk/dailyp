from django.contrib.auth.models import User
from django.http import Http404
import models
import db_cbs

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Poster(APIView):

    def post(self, request, format=None):
        rest_model = models.HomeModel()

        cbs = db_cbs.CBS()
        if cbs.connect():
            rest_model.debug_message = request.data
            cbs.post_run(request.data)
        else:
            rest_model.debug_message = {"Mesessage": "Error posting to Dailyp"}
        return Response(rest_model.debug_message, status=status.HTTP_201_CREATED)