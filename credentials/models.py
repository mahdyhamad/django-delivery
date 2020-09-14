from django.db import models
from model_utils.models import TimeStampedModel


class Credentials(TimeStampedModel):
    drop_off_cred = models.TextField()
    pickup_cred = models.TextField()
    valid_drop = models.BooleanField(default=False)
    valid_pickup = models.BooleanField(default=False)

    @classmethod
    def create(cls):
        from utils.utils import get_random_alphanumeric_string as rand
        cred = cls.objects.create(drop_off_cred=rand(5), pickup_cred=rand(5))
        return cred

    def validate_drop_off_key(self, key, *args, **kwargs):
        if key == self.drop_off_cred:
            self.valid_drop = True
            self.save()
            return True
        else:
            return False

    def validate_pickup_key(self, key, *args, **kwargs):
        if key == self.pickup_cred:
            if not self.valid_drop:
                raise Exception("Drop Off is not verified")
            self.valid_pickup = True
            self.save()
            return True

        return False

