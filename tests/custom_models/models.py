from django.db import models


class ModelWithCustomPermissions(models.Model):
    name = models.TextField()

    class Meta:
        permissions = [
            ("can_do_something", "Can do something"),
        ]
