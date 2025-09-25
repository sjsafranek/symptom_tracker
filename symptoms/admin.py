from django.contrib import admin

from . import models

# admin.site.register(models.Agency)
 
# from guardian.admin import GuardedModelAdmin
#
# class SymptomScoreAdmin(GuardedModelAdmin):
#     pass
#
# admin.site.register(models.SymptomScore, SymptomScoreAdmin)




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
    	'client', 
    	'therapist',
    	'display'
    ]
    list_display_links = ['client', 'therapist', 'display']
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(models.ClientNote, ClientNoteAdmin)



class ClientSymptomAdmin(admin.ModelAdmin):
    list_display = [
    	'client', 
    	'description',
    	'is_active'
    ]
    list_display_links = ['client', 'description']

admin.site.register(models.ClientSymptom, ClientSymptomAdmin)



class ClientSessionAdmin(admin.ModelAdmin):
    list_display = [
    	'date',
    	'client',
    	'therapist',
    	'no_show'
    ]
    list_display_links = ['client', 'therapist', 'date']

admin.site.register(models.ClientSession, ClientSessionAdmin)



class ClientSessionSymptomScoreAdmin(admin.ModelAdmin):
    list_display = [
    	'session__date',
    	'session__client',
    	'session__therapist',
    	'symptom__description',
    	'rank'
    ]
    list_display_links = ['session__date', 'session__client', 'session__therapist', 'symptom__description']

admin.site.register(models.ClientSessionSymptomScore, ClientSessionSymptomScoreAdmin)



# admin.site.register(models.ClientSessionProtocolSiteTraining)
admin.site.register(models.ClientSessionProtocolSiteTrainingILF)
admin.site.register(models.ClientSessionProtocolSiteTrainingAlphaTheta)
admin.site.register(models.ClientSessionProtocolSiteTrainingFrequencyBand)
admin.site.register(models.ClientSessionProtocolSiteTrainingSynchrony)
