from django.contrib.auth.forms import UserCreationForm
from users.models import User


class CreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'username', 'last_name', 'email', 'password')