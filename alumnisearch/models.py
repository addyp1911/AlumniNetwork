from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.core import validators
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid
from .utils import url_validator

# Create your models here.
class BaseModel(models.Model):
    """A base model to deal with all the abstract level model creations"""
    class Meta:
        abstract = True

    # uuid field
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    # date fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Create a user model
class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """A ORM for users interactions"""
    class Meta:
        """A meta object for defining name of the user table"""
        db_table = "user"
    
    full_name = models.CharField(max_length=100)
    profile_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True, default='')
    password = models.CharField(max_length=100)
    school = models.CharField(max_length=200, blank=True, null=True)
    batch_year = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ('full_name', 'school', 'password', 'email', 'batch_year')

    def __str__(self):

        """Return string representation of user object"""
        return str(self.uuid) + " " + str(self.full_name)

    # use User manager to manage create user and super user
    objects = UserManager()

    # define required fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class AlumnusProfile(BaseModel):

    GENDER_CHOICES = (('male','male'), ('female','female'), ('other', 'other'))

    alumnus = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(max_length=100, null=True, blank=True, default='default-avatar.png', upload_to="static")
    dob = models.DateField(null=True, blank=True)
    mobile = PhoneNumberField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    website_url = models.CharField(max_length=50, null=True, blank=True, validators=[url_validator])
    description = models.TextField(max_length=500,null=True, blank=True)

    def __str__(self):

        """Return string representation of alumnusprofile object"""
        return str(self.uuid) + str(self.alumnus.full_name)
