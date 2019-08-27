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

    def get_serialized_model(self):
        datapoints = [datapoint.get_serialized_model() for datapoint in Datapoint.objects.filter(plant_id=self.id)]
        return {
            'id': self.id,
            'name': self.name,
            'datapoints': datapoints
        }

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"


class Datapoint(models.Model):
    id = models.AutoField(primary_key=True)
    plant = models.ForeignKey(
        Plant,
        verbose_name="Plant",
        related_name="plant_datapoints",
        on_delete=models.CASCADE
    )
    energy_expected = models.DecimalField(decimal_places=14)
    energy_observed = models.DecimalField(decimal_places=14)
    irradiation_expected = models.DecimalField(decimal_places=14)
    irradiation_observed = models.DecimalField(decimal_places=14)

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
            }
        }