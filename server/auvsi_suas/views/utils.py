"""Utilities for admins."""

import json
import logging
from LatLon23 import string2latlon
from auvsi_suas.proto import interop_admin_api_pb2
from auvsi_suas.views.decorators import require_superuser
from auvsi_suas.views.json import ProtoJsonEncoder
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic import View
from google.protobuf import json_format

LATLON_FORMAT = 'H%d%-%m%-%S'


class GpsConversion(View):
    """Converts GPS from string to decimal."""

    @method_decorator(require_superuser)
    def dispatch(self, *args, **kwargs):
        return super(GpsConversion, self).dispatch(*args, **kwargs)

    def post(self, request):
        request_proto = interop_admin_api_pb2.GpsConversionRequest()
        try:
            json_format.Parse(request.body, request_proto)
        except Exception as e:
            return HttpResponseBadRequest('Failed to parse request. Error: %s' % str(e))

        if not request_proto.HasField('latitude') or not request_proto.HasField('longitude'):
            return HttpResponseBadRequest('Request missing fields.')

        try:
            latlon = string2latlon(request_proto.latitude, request_proto.longitude, LATLON_FORMAT)
        except Exception as e:
            return HttpResponseBadRequest('Failed to convert GPS. Error: %s' % str(e))

        response = interop_admin_api_pb2.GpsConversionResponse()
        response.latitude = latlon.lat.decimal_degree
        response.longitude = latlon.lon.decimal_degree

        return HttpResponse(
            json_format.MessageToJson(response),
            content_type="application/json")
