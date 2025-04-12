from django.contrib import admin

from .models import TimeSpent, Skill

# 
class TimeSpentInline(admin.TabularInline):
    model = TimeSpent

# class SkillAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["skill_name"]}),
    #     ("Date information", {"fields", ["pub_date"]}),
    # ]
    # inlines = [TimeSpentInline]
    # list_display = ["skill_name", "Pub_date" ]



admin.site.register(Skill)
