from django.contrib import admin
from users.models import Subscriber, User
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "email")
    list_filter = ("first_name", "email")

    class Meta:
        verbose_name_plural = "Пользователи"


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author"
    )

    class Meta:
        verbose_name_plural = "Подписчики"


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.unregister(Group)
