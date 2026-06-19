from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, default='profile_images/noimage.jpg')
    phone = models.CharField(blank=True)
    # subscription = models.ForeignKey(to=Subscription,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField(unique=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return {f"{self.first_name} {self.last_name}"}

    def __str__(self):
        return self.username

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"






