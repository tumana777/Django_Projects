from django.shortcuts import render, get_object_or_404, redirect
from communication.forms import SmartphoneForm
from computers.forms import PCForm, LaptopForm, TabletForm, PartsOrAccessoriesForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import MainCategory, Category, SubCategory

def fetch_categories(request):
    maincategory_id = request.GET.get('maincategory_id')
    categories = Category.objects.filter(maincategory_id=maincategory_id)
    category_data = [{'id': category.id, 'name': category.name} for category in categories]
    return JsonResponse({'categories': category_data})

def fetch_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id)
    subcategory_data = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]
    return JsonResponse({'subcategories': subcategory_data})

def add_product(request):
    maincategories = MainCategory.objects.all()

    form_mapping = {
        'pc': (PCForm, 1, 'category'),
        'laptop': (LaptopForm, 2, 'category'),
        'tablet': (TabletForm, 3, 'category'),
        'smartphone': (SmartphoneForm, 8, 'category'),
        'mouse': (PartsOrAccessoriesForm, 5, 'subcategory'),
        'web camera': (PartsOrAccessoriesForm, 6, 'subcategory'),
        'mouse pad': (PartsOrAccessoriesForm, 7, 'subcategory'),
        'pc speakers': (PartsOrAccessoriesForm, 8, 'subcategory'),
        'usb gadget': (PartsOrAccessoriesForm, 9, 'subcategory'),
        'pc microphone': (PartsOrAccessoriesForm, 10, 'subcategory'),
        'laptop cooler': (PartsOrAccessoriesForm, 14, 'subcategory'),
        'laptop holder': (PartsOrAccessoriesForm, 15, 'subcategory'),
        'laptop case': (PartsOrAccessoriesForm, 16, 'subcategory'),
        'processor': (PartsOrAccessoriesForm, 17, 'subcategory'),
        'cooler': (PartsOrAccessoriesForm, 18, 'subcategory'),
        'sound board': (PartsOrAccessoriesForm, 19, 'subcategory'),
        'motherboard': (PartsOrAccessoriesForm, 20, 'subcategory'),
        'video card': (PartsOrAccessoriesForm, 21, 'subcategory'),
        'power supply': (PartsOrAccessoriesForm, 22, 'subcategory'),
        'thermal paste': (PartsOrAccessoriesForm, 23, 'subcategory'),
        'hdd': (PartsOrAccessoriesForm, 24, 'subcategory'),
        'ssd': (PartsOrAccessoriesForm, 25, 'subcategory'),
        'keyboard': (PartsOrAccessoriesForm, 26, 'subcategory'),
        'processor': (PartsOrAccessoriesForm, 27, 'subcategory'),
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        form_class, category_id, category_field = form_mapping.get(form_type, (None, None, None))

        if form_class:
            form = form_class(request.POST)
            if category_field == 'category':
                form.instance.category_id = category_id
            elif category_field == 'subcategory':
                form.instance.subcategory_id = category_id

            if form.is_valid():
                form.instance.owner = request.user
                form.save()
                return redirect('success_page')

    return render(request, 'mainapp/add_product.html', {'maincategories': maincategories})

def load_form(request):
    category_id = request.GET.get('category_id')
    subcategory_id = request.GET.get('subcategory_id')
    form_html = ''
    form_type = ''

    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            if category.name.lower() == 'pc':
                form = PCForm()
                form_type = 'pc'
            elif category.name.lower() == 'laptops':
                form = LaptopForm()
                form_type = 'laptop'
            elif category.name.lower() == 'tablets':
                form = TabletForm()
                form_type = 'tablet'
            elif category.name.lower() == 'smartphones':
                form = SmartphoneForm()
                form_type = 'smartphone'
            else:
                form = None

            if form:
                form_html = render_to_string('mainapp/form_template.html', {'form': form, 'form_type': form_type}, request=request)
        except Category.DoesNotExist:
            pass

    if subcategory_id:
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            category = subcategory.category
            
            if subcategory.name.lower() == 'mouse':
                form = PartsOrAccessoriesForm()
                form_type = 'mouse'
            elif subcategory.name.lower() == 'web camera':
                form = PartsOrAccessoriesForm()
                form_type = 'web camera'
            elif subcategory.name.lower() == 'mouse pad':
                form = PartsOrAccessoriesForm()
                form_type = 'mouse pad'
            elif subcategory.name.lower() == 'pc speakers':
                form = PartsOrAccessoriesForm()
                form_type = 'pc speakers'
            elif subcategory.name.lower() == 'usb gadget':
                form = PartsOrAccessoriesForm()
                form_type = 'usb gadget'
            elif subcategory.name.lower() == 'pc microphone':
                form = PartsOrAccessoriesForm()
                form_type = 'pc microphone'
            elif subcategory.name.lower() == 'laptop cooler':
                form = PartsOrAccessoriesForm()
                form_type = 'laptop cooler'
            elif subcategory.name.lower() == 'laptop holder':
                form = PartsOrAccessoriesForm()
                form_type = 'laptop holder'
            elif subcategory.name.lower() == 'laptop case':
                form = PartsOrAccessoriesForm()
                form_type = 'laptop case'
            elif subcategory.name.lower() == 'processor':
                form = PartsOrAccessoriesForm()
                form_type = 'processor'
            elif subcategory.name.lower() == 'cooler':
                form = PartsOrAccessoriesForm()
                form_type = 'cooler'
            elif subcategory.name.lower() == 'sound board':
                form = PartsOrAccessoriesForm()
                form_type = 'sound board'
            elif subcategory.name.lower() == 'motherboard':
                form = PartsOrAccessoriesForm()
                form_type = 'motherboard'
            elif subcategory.name.lower() == 'video card':
                form = PartsOrAccessoriesForm()
                form_type = 'video card'
            elif subcategory.name.lower() == 'power supply':
                form = PartsOrAccessoriesForm()
                form_type = 'power supply'
            elif subcategory.name.lower() == 'thermal paste':
                form = PartsOrAccessoriesForm()
                form_type = 'thermal paste'
            elif subcategory.name.lower() == 'hdd':
                form = PartsOrAccessoriesForm()
                form_type = 'hdd'
            elif subcategory.name.lower() == 'ssd':
                form = PartsOrAccessoriesForm()
                form_type = 'ssd'
            elif subcategory.name.lower() == 'keyboard':
                form = PartsOrAccessoriesForm()
                form_type = 'keyboard'
            elif subcategory.name.lower() == 'laptop battery':
                form = PartsOrAccessoriesForm()
                form_type = 'laptop battery'
            else:
                form = None

            if form:
                form_html = render_to_string('mainapp/form_template.html', {'form': form, 'form_type': form_type}, request=request)
        except SubCategory.DoesNotExist:
            pass

    return JsonResponse({'form_html': form_html})

def success_page(request):
    return render(request, 'mainapp/success.html')
