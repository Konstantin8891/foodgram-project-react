from django.contrib import admin

from users.models import User, Subscriber


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'email'
    )
    list_filter = ('first_name', 'email')


class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscriber, SubscriberAdmin)