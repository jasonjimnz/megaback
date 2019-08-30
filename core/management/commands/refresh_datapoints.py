import datetime

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from core.models import Datapoint, Plant


class Command(BaseCommand):
    help = 'Checks the Panel Management API for refreshing all the panels'

    @classmethod
    def get_datapoints_from_plant(cls, plant_id):
        monitor_url = "{base_url}?plant-id={plant_id}&from={from_date}&to={to_date}"
        to_date = datetime.date.today()
        from_date = to_date - datetime.timedelta(days=1)
        monitor_request = requests.get(
            url=monitor_url.format(
                base_url=settings.MONITORING_SERVICE_URL,
                plant_id=plant_id,
                from_date=from_date.isoformat(),
                to_date=to_date.isoformat()
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

    def handle(self, *args, **options):
        for plant in Plant.objects.all():
            self.get_datapoints_from_plant(plant.id)
            self.stdout.write(self.style.SUCCESS('Successfully updated plant "%s" datapoints' % plant.name))
