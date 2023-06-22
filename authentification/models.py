from django.conf import settings
from django.db import models



"""class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_manager = models.BooleanField('Is customer', default=False)
    is_customer = models.BooleanField('Is employee', default=False)

    # Add related_name to resolve clash with auth.User.groups
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='authentification_user_set',
        related_query_name='authentification_user',
        verbose_name='groups'
    )

    # Add related_name to resolve clash with auth.User.user_permissions
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='authentification_user_set',
        related_query_name='authentification_user',
        verbose_name='user permissions'
    )"""


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registration_model'
    )

