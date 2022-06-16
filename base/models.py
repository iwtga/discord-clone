from django.db import models

# Create your models here.
class Room(models.Model):
    # host =
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # topic =
    # participants =
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name