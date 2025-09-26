from django.contrib import admin
import django.urls
import django.utils.html

from . import models

# admin.site.register(models.Agency)
 
# from guardian.admin import GuardedModelAdmin
#
# class SymptomScoreAdmin(GuardedModelAdmin):
#     pass
#
# admin.site.register(models.SymptomScore, SymptomScoreAdmin)


APP_LABEL = 'symptoms'


admin.site.register(models.SymptomCategory)


class TherapistAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']
    list_display_links = ['user']
    search_fields =  ['first_name', 'last_name']
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(models.Therapist, TherapistAdmin)



class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']
    list_display_links = ['user']
    search_fields =  ['first_name', 'last_name']
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(models.Client, ClientAdmin)



class ClientNoteAdmin(admin.ModelAdmin):
    list_display = [
        'updated_at',
        'link_to_client', 
        'link_to_therapist',
        'display'
    ]
    list_display_links = ['link_to_therapist', 'link_to_therapist', 'display']
    readonly_fields = ('created_at', 'updated_at')
   
    def link_to_client(self, obj):
        view_name = f"admin:{APP_LABEL}_{'client'}_change"
        link = django.urls.reverse(view_name, args=[obj.client.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.client)
    link_to_client.short_description = 'Client'    

    def link_to_therapist(self, obj):
        view_name = f"admin:{APP_LABEL}_{'therapist'}_change"
        link = django.urls.reverse(view_name, args=[obj.therapist.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.therapist)
    link_to_therapist.short_description = 'Therapist'        

admin.site.register(models.ClientNote, ClientNoteAdmin)



class ClientSymptomAdmin(admin.ModelAdmin):
    list_display = [
        'link_to_client', 
        'description',
        'is_active'
    ]
    list_display_links = ['link_to_client', 'description']

    def link_to_client(self, obj):
        view_name = f"admin:{APP_LABEL}_{'client'}_change"
        link = django.urls.reverse(view_name, args=[obj.client.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.client)
    link_to_client.short_description = 'Client'    

admin.site.register(models.ClientSymptom, ClientSymptomAdmin)



class ClientSessionAdmin(admin.ModelAdmin):
    list_display = [
        'date',
        'number',
        'link_to_client',
        'link_to_therapist',
        'no_show'
    ]
    list_display_links = ['link_to_client', 'link_to_therapist', 'number', 'date']

    def link_to_client(self, obj):
        view_name = f"admin:{APP_LABEL}_{'client'}_change"
        link = django.urls.reverse(view_name, args=[obj.client.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.client)
    link_to_client.short_description = 'Client'    

    def link_to_therapist(self, obj):
        view_name = f"admin:{APP_LABEL}_{'therapist'}_change"
        link = django.urls.reverse(view_name, args=[obj.therapist.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.therapist)
    link_to_therapist.short_description = 'Therapist'     

admin.site.register(models.ClientSession, ClientSessionAdmin)



class ClientSessionSymptomScoreAdmin(admin.ModelAdmin):
    list_display = [
        'link_to_session',
        'link_to_client',
        'link_to_symptom',
        'score'
    ]
    list_display_links = ['link_to_session', 'link_to_client', 'link_to_symptom', 'score']

    def link_to_session(self, obj):
        view_name = f"admin:{APP_LABEL}_{'clientsession'}_change"
        link = django.urls.reverse(view_name, args=[obj.session_id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.session.date)
    link_to_session.short_description = 'Session'

    def link_to_client(self, obj):
        view_name = f"admin:{APP_LABEL}_{'client'}_change"
        link = django.urls.reverse(view_name, args=[obj.session.client.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.session.client)
    link_to_client.short_description = 'Client'    

    def link_to_symptom(self, obj):
        view_name = f"admin:{APP_LABEL}_{'clientsymptom'}_change"
        link = django.urls.reverse(view_name, args=[obj.symptom.id])
        return django.utils.html.format_html('<a href="{}">{}</a>', link, obj.symptom.description)
    link_to_symptom.short_description = 'Symptom'        

admin.site.register(models.ClientSessionSymptomScore, ClientSessionSymptomScoreAdmin)



# admin.site.register(models.ClientSessionProtocolSiteTraining)
admin.site.register(models.ClientSessionProtocolSiteTrainingILF)
admin.site.register(models.ClientSessionProtocolSiteTrainingAlphaTheta)
admin.site.register(models.ClientSessionProtocolSiteTrainingFrequencyBand)
admin.site.register(models.ClientSessionProtocolSiteTrainingSynchrony)
