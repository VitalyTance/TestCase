from django.test import TestCase
from django.core.validators import ValidationError
from django.db.utils import IntegrityError

from .models import RobotModelDB, RobotVersionDB
# Create your tests here.


class RobotModelDBTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        RobotModelDB.objects.create(model='R2')

    def test_max_length_equals_2(self):
        # Проверка максимальной длины поля в 2 символа
        robot = RobotModelDB.objects.get(id=1)
        max_length = robot._meta.get_field('model').max_length
        self.assertEqual(max_length, 2)

    def test_model_name_unique(self):
        # Проверка уникальности поля
        with self.assertRaises(IntegrityError):
            RobotModelDB.objects.create(model='R2')

    def test_model_cannot_be_blank(self):
        # Проверка невозможности ввести пустое поле
        robot = RobotModelDB(model=None)
        with self.assertRaises(ValidationError):
            if robot.full_clean():
                robot.save()
        self.assertEqual(RobotModelDB.objects.filter(model=None).count(), 0)

    def test_model_cannot_be_cyrillic(self):
        # Проверка невозможности ввести кириллицу в поле
        robot = RobotModelDB(model='Ш1')
        with self.assertRaises(ValidationError):
            if robot.full_clean():
                robot.save()
        self.assertEqual(RobotModelDB.objects.filter(model='Ш1').count(), 0)


class RobotVersionDBTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        robot = RobotModelDB.objects.create(model='R2')
        RobotVersionDB.objects.create(model=robot,
                                      version='D2')

    def test_robot_version_max_length(self):
        # Проверка длину поля version в 2 символа
        version = RobotVersionDB.objects.get(id=1)
        max_length = version._meta.get_field('version').max_length
        self.assertEqual(max_length, 2)

    def test_robot_version_cannot_be_cyrillic(self):
        # Проврека невозможности ввести в поле кириллицу
        version = RobotVersionDB(version='Л3')
        with self.assertRaises(ValidationError):
            if version.full_clean():
                version.save()
        self.assertEqual(RobotVersionDB.objects.filter(version='Л3').count(), 0)

    def test_robot_version_cannot_be_null(self):
        # Проврека невозможности оставить поле пустым
        version = RobotVersionDB(version=None)
        with self.assertRaises(ValidationError):
            if version.full_clean():
                version.save()
        self.assertEqual(RobotVersionDB.objects.filter(version=None).count(), 0)
