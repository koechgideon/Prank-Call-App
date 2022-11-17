from django.contrib import admin
from .models import Prank, History, Tokens, Otp

admin.site.register(Prank)
admin.site.register(History)
admin.site.register(Tokens)
admin.site.register(Otp)