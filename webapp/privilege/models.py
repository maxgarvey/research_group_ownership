from django.contrib.auth.models import User
from django.db import models

class privilege(models.Model):
    field = models.CharField(max_length=1)
    class Meta:
        permissions = (
            ('webapp', 'privileged'),
        )
