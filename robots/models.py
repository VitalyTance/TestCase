import datetime

from django.db import models
from django.core.validators import RegexValidator


regex_robot_db_fields = RegexValidator(r'^[A-Z0-9]{2}$',
                                       'Допустимы только прописные латинские символы и цифры')


class RobotModelDB(models.Model):
    """
    Модель, созданная для вненения модели робота в
    базу данных завода
    """
    model = models.CharField(verbose_name='Модель робота', max_length=2, blank=False, null=False,
                             validators=[regex_robot_db_fields], unique=True)

    def __str__(self):
        return self.model


class RobotVersionDB(models.Model):
    """
    Модель, созданная для внесения серии модели робота в
    базу данных завода
    """
    model = models.ForeignKey(RobotModelDB, verbose_name='Модель робота',
                              related_name='versions', on_delete=models.CASCADE)
    version = models.CharField(verbose_name='Версия робота', max_length=2, blank=False, null=False,
                               validators=[regex_robot_db_fields])

    def __str__(self):
        return self.version


class Robot(models.Model):
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    serial = models.CharField(max_length=5, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.serial = self.model + '-' + self.version
        return super(Robot, self).save(*args, **kwargs)


class RobotOffer(models.Model):
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    serial = models.CharField(max_length=5, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.serial = self.model + '-' + self.version
        return super(RobotOffer, self).save(*args, **kwargs)


class RobotRelease(models.Model):
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    serial = models.CharField(max_length=5, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.serial = self.model + '-' + self.version
        return super(RobotRelease, self).save(*args, **kwargs)
