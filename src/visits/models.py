from django.db import models


class NonDeleted(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)
    everything = models.Manager()
    objects = NonDeleted()

    class Meta:
        abstract = True

    def soft_deleted(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()


class Visit(SoftDelete):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    date = models.DateTimeField()
    title = models.CharField(max_length=50)
    is_paid = models.BooleanField(default=False)
