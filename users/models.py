from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)

        # Auto-generate username if not provided
        if not extra_fields.get('username'):
            base_username = email.split('@')[0]
            username = slugify(base_username.replace('.', '_'))
            counter = 1
            while self.model.objects.filter(username=username).exists():
                username = f"{slugify(base_username.replace('.', '_'))}_{counter}"
                counter += 1
            extra_fields['username'] = username

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.TextChoices):
        FARMER = 'FARMER', _('Farmer')
        COLD_ROOM_OWNER = 'COLD_ROOM_OWNER', _('Cold Room Owner')

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_('Username'),
        null=True,
        blank=True,
        help_text=_("Automatically generated from email")
    )
    email = models.EmailField(_('email address'), unique=True)

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        verbose_name=_('User Type')
    )
    phone = PhoneNumberField(
        null=False,
        blank=False,
        unique=True,
        verbose_name=_('Phone Number')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']

    objects = UserManager()

    def _generate_username(self):
        base_username = self.email.split('@')[0]
        return slugify(base_username.replace('.', '_'))

    def save(self, *args, **kwargs):
        if not self.username:
            base = self._generate_username()
            self.username = base
            counter = 1
            while User.objects.filter(username=self.username).exists():
                self.username = f"{base}_{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.get_full_name()} - {self.user_type}"
