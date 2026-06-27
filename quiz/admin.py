from django.contrib import admin
from .models import Course, Question, Option

class OptionInline(admin.TabularInline):
    model = Option
    extra = 4
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', "course")
    inlines = [OptionInline]
    list_per_page = 20

admin.site.register(Course)
admin.site.register(Question, QuestionAdmin)
admin.site.site_header = "Quiz Administration"
admin.site.site_title = "Quiz App Administration"
admin.site.index_title =  "Quiz App Administration"