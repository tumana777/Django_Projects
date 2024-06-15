from django.contrib import admin

from .models import ScreenSize, OS, CPU, GPU, Cooling, LaptopBrand, LaptopModel, PCType, PC, Laptop, Tablet, PartsOrAccessories

admin.site.register(ScreenSize)
admin.site.register(OS)
admin.site.register(CPU)
admin.site.register(GPU)
admin.site.register(Cooling)
admin.site.register(LaptopBrand)
admin.site.register(LaptopModel)
admin.site.register(PCType)
admin.site.register(PC)
admin.site.register(Laptop)
admin.site.register(Tablet)
admin.site.register(PartsOrAccessories)
