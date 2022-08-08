from django.db import models


class Auth(models.Model):
    method = models.CharField(
        max_length=50,
        choices=[
            ('JWT', 'JWT'),
            ('OAuth', 'OAuth')
            ]
        )
