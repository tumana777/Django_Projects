from django.contrib import admin
from .models import SmartphoneBrand, SmartphoneModel, SmartphoneMainCamera, SmartphoneSelfieCamera, SmartphoneOS, Smartphone

admin.site.register(SmartphoneBrand)
admin.site.register(SmartphoneModel)
admin.site.register(SmartphoneMainCamera)
admin.site.register(SmartphoneSelfieCamera)
admin.site.register(SmartphoneOS)
admin.site.register(Smartphone)
