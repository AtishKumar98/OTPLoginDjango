from django.db import models
# from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User



phone_regex = RegexValidator(regex=r'^\+?\d{9,15}$',message="Phone must be entered in the format +99999999, Upto 15 digits allowed")


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[phone_regex],max_length=17,unique=True)


