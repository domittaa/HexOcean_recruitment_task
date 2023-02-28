from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator

from django.db import models


class Tier(models.Model):
    name = models.CharField(max_length=50)
    thumbnail_sizes = models.CharField(max_length=255, default="200")
    link_present = models.BooleanField()
    allow_expiring_link = models.BooleanField()

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    account_tier = models.ForeignKey(Tier, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    original_image = models.ImageField(
        upload_to="media/originals/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_image.name


class Thumbnail(models.Model):
    path = models.TextField()
    size = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="thumbnails")

    # def __str__(self):
    #     return self.image.original_image.name


class ExpiringLinks(models.Model):
    code = models.CharField(max_length=100)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    time = models.DateTimeField()
    seconds = models.IntegerField(validators=[
            MaxValueValidator(3000),
            MinValueValidator(300)
        ])
