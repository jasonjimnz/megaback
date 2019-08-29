import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse, QueryDict
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from core.models import Datapoint, Plant


class CoreBaseView(View):
    version = settings.VERSION

    def dispatch(self, request, *args, **kwargs) -> JsonResponse:
        return super(CoreBaseView, self).dispatch(request)

    def get(self, request, *args, **kwargs) -> JsonResponse:
        return self.rest_not_found_response()

    @classmethod
    def rest_not_found_response(cls, message: str = 'Endpoint not found') -> JsonResponse:
        return JsonResponse(
            {'message': message},
            status=404,
            safe=False,
            json_dumps_params={'indent': 2}
        )

    @classmethod
    def success_response(cls, data: dict = None) -> JsonResponse:
        return JsonResponse(
            data,
            status=200,
            safe=False,
            json_dumps_params={'indent': 2}
        )

    @classmethod
    def bad_request_response(cls, message: str):
        return JsonResponse(
            {'message': message},
            status=400,
            safe=False,
            json_dumps_params={'indent': 2}
        )

    @classmethod
    def created_response(cls, data):
        return JsonResponse(
            data,
            status=201,
            safe=False,
            json_dumps_params={'indent': 2}
        )


class MonitoringServiceView(CoreBaseView):

    def get(self, request,  *args, **kwargs) -> JsonResponse:
        monitor_url = "{base_url}?plant-id={plant_id}&from={from_date}&to={to_date}"
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        plant_id = self.kwargs.get('plant_id')
        if from_date and to_date and plant_id:
            monitor_request = requests.get(
                url=monitor_url.format(
                    base_url=settings.MONITORING_SERVICE_URL,
                    plant_id=plant_id,
                    from_date=from_date,
                    to_date=to_date
                )
            )
            if monitor_request.status_code == 200:
                monitor_response_datapoints = monitor_request.json()
                response = []
                for datapoint in monitor_response_datapoints:
                    datapoint['plant_id'] = plant_id
                    response.append(
                        Datapoint.objects.check_or_create_datapoint(
                            **datapoint
                        ).get_serialized_model()
                    )
                return self.success_response({'datapoints': response})

        return self.bad_request_response('Plant ID, and dates in ISO-8061 format are required')


class PlantView(CoreBaseView):
    plant_id = None
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.plant_id = self.kwargs.get('plant_id')
        return super(PlantView, self).dispatch(request)

    def get(self, request, *args, **kwargs):
        if self.plant_id:
            try:
                plant = Plant.objects.get(id=self.plant_id)
            except ObjectDoesNotExist:
                return self.rest_not_found_response('Plant not found')
            return self.success_response({'plant': plant.get_serialized_model()})
        plants = [plant.get_serialized_model(show_datapoints=False) for plant in Plant.objects.all()]
        return self.success_response({'plants': plants})

    def post(self, request, *args, **kwargs):
        if self.plant_id or self.request.method == 'GET':
            return self.rest_not_found_response()
        plant_name = request.POST.get('name')
        if plant_name:
            plant = Plant(name=plant_name)
            try:
                plant.save()
            except IntegrityError:
                return self.bad_request_response(
                    'There is a plant with {name} as name'.format(
                        name=plant_name
                    )
                )
            return self.created_response(plant.get_serialized_model())
        return self.bad_request_response('Name is required for plant')

    def put(self, request, *args, **kwargs):
        if not self.plant_id:
            return self.rest_not_found_response()
        plant_name = QueryDict(request.body).get('name')
        if not plant_name:
            return self.bad_request_response('Name is required for plant')
        try:
            plant = Plant.objects.get(id=self.plant_id)
            plant.name = plant_name
            try:
                plant.save()
                return self.created_response(plant.get_serialized_model())
            except IntegrityError:
                return self.bad_request_response(
                    'There is a plant with {name} as name'.format(
                        name=plant_name
                    )
                )
        except ObjectDoesNotExist:
            return self.rest_not_found_response('Plant does not exist')

    def delete(self, request, *args, **kwargs):
        if not self.plant_id:
            return self.rest_not_found_response()
        try:
            plant = Plant.objects.get(id=self.plant_id)
            plant.delete()
            return self.success_response({'deleted': True})
        except ObjectDoesNotExist:
            return self.rest_not_found_response('Plant does not exist')
