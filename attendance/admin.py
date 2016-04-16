from django.contrib import admin
from attendance.models import Session, Swipe
from django.forms import ModelForm

class SwipeInline(admin.TabularInline):
	model = Swipe

class SessionAdmin(admin.ModelAdmin):
	inlines = [
		SwipeInline,
		]

admin.site.register(Session, SessionAdmin)
admin.site.register(Swipe)