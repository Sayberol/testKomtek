from django.contrib import admin

from mainapp.models import Directory, DirectoryElement
from users.models import User

admin.site.register(User)
admin.site.register(Directory)
admin.site.register(DirectoryElement)
