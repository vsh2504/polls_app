from django.contrib import admin
from .models import Question,Choice
# Register your models here.

#SIMPLE REGISTRATION
# admin.site.register(Question)
admin.site.register(Choice)

# CUSTOMISING THE ADMIN FORM
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date','question_text']
#
# admin.site.register(Question,QuestionAdmin)

#HOW TO ADD CHOICES WITH QUESTIONS

#Stacked Inline View Of Options
# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3

#Tabular Inline VIEW
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    #display individual fields in admin "change list":- list_display
    list_display = ('question_text','pub_date','was_published_recently')

    #adds a “Filter” sidebar that lets people filter the change list by the pub_date field
    list_filter = ['pub_date']

    #add some search capability
    search_fields = ['question_text']

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'],'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
