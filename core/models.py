import datetime

import pytz
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
# Create your models here.


class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=512,
        verbose_name="Name",
        help_text="Plant name",
        unique=True
    )

    def __str__(self):
        return self.name

    def get_serialized_model(self, show_datapoints=True):
        if show_datapoints:
            datapoints = [datapoint.get_serialized_model() for datapoint in Datapoint.objects.filter(plant_id=self.id)]
            return {
                'id': self.id,
                'name': self.name,
                'datapoints': datapoints
            }
        return {
                'id': self.id,
                'name': self.name
            }

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"


class DatapointManager(models.Manager):
    def check_or_create_datapoint(self, **kwargs):
        try:
            datapoint_datetime = datetime.datetime.strptime(
                kwargs.get('datetime'),
                "%Y-%m-%dT%H:%M:%S%z"
            ).astimezone(pytz.timezone(settings.TIME_ZONE))
        except ValueError:
            datapoint_datetime = datetime.datetime.strptime(
                kwargs.get('datetime'),
                "%Y-%m-%dT%H:%M:%S"
            ).astimezone(pytz.timezone(settings.TIME_ZONE))
        try:
            model = self.get_queryset().get(
                plant_id=kwargs.get('plant_id'),
                datetime= datapoint_datetime
            )
        except ObjectDoesNotExist:
            model = self.model(
                plant_id=kwargs.get('plant_id'),
                datetime=datapoint_datetime,
                energy_expected=kwargs.get('expected').get('energy'),
                energy_observed=kwargs.get('observed').get('energy'),
                irradiation_expected=kwargs.get('expected').get('irradiation'),
                irradiation_observed=kwargs.get('observed').get('irradiation'),
            )
            model.save()
        return model


class Datapoint(models.Model):
    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(
        Plant,
        verbose_name="Plant",
        related_name="plant_datapoints",
        on_delete=models.CASCADE
    )
    energy_expected = models.DecimalField(decimal_places=14, max_digits=17)
    energy_observed = models.DecimalField(decimal_places=14, max_digits=17)
    irradiation_expected = models.DecimalField(decimal_places=14, max_digits=17)
    irradiation_observed = models.DecimalField(decimal_places=14, max_digits=17)
    datetime = models.DateTimeField(
        verbose_name="Datetime",
        help_text="Datapoint extraction datetime",
        null=True,
        blank=True
    )

    objects = DatapointManager()

    def get_serialized_model(self):
        return {
            'id': self.id,
            'plant_id': self.plant_id,
            'expected': {
                'energy': float(self.energy_expected),
                'irradiation': float(self.irradiation_expected)
            },
            'observed': {
                'energy': float(self.energy_observed),
                'irradiation': float(self.irradiation_observed)
            },
            'datetime': self.datetime.isoformat() if self.datetime else None
        }

    class Meta:
        verbose_name = "Datapoint"
        verbose_name_plural = "Datapoints"
        unique_together = ('plant', 'datetime')