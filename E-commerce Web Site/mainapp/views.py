from django.shortcuts import render, get_object_or_404, redirect
from communication.forms import SmartphoneForm
from computers.forms import PCForm, LaptopForm, TabletForm, PartsOrAccessoriesForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import MainCategory, Category, SubCategory
from django.views.generic import ListView
from computers.models import PC, Laptop, Tablet

class MainCategoryListView(ListView):
    model = MainCategory
    template_name = "mainapp/maincategories.html"
    context_object_name = "maincategories"

class CategoryListView(ListView):
    model = Category
    template_name = "mainapp/categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        maincategory_name = self.kwargs['maincategory_name']
        maincategory = get_object_or_404(MainCategory, name=maincategory_name)
        return Category.objects.filter(maincategory=maincategory)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maincategory'] = get_object_or_404(MainCategory, name=self.kwargs['maincategory_name'])
        context['PCs'] = PC.objects.all()
        context['laptops'] = Laptop.objects.all()
        context['tablets'] = Tablet.objects.all()
        return context

class SubCategoryListView(ListView):
    model = SubCategory
    template_name = "mainapp/subcategories.html"
    context_object_name = "subcategories"

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = get_object_or_404(Category, name=category_name)
        return SubCategory.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, name=self.kwargs['category_name'])
        context['maincategory'] = get_object_or_404(MainCategory, name=self.kwargs['maincategory_name'])
        context['PCs'] = PC.objects.all()
        context['laptops'] = Laptop.objects.all()
        context['tablets'] = Tablet.objects.all()
        return context


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

    category_forms = {
        'pc': (PCForm, 'pc'),
        'laptops': (LaptopForm, 'laptop'),
        'tablets': (TabletForm, 'tablet'),
        'smartphones': (SmartphoneForm, 'smartphone')
    }

    subcategory_forms = {
        'mouse': 'mouse',
        'web camera': 'web camera',
        'mouse pad': 'mouse pad',
        'pc speakers': 'pc speakers',
        'usb gadget': 'usb gadget',
        'pc microphone': 'pc microphone',
        'laptop cooler': 'laptop cooler',
        'laptop holder': 'laptop holder',
        'laptop case': 'laptop case',
        'processor': 'processor',
        'cooler': 'cooler',
        'sound board': 'sound board',
        'motherboard': 'motherboard',
        'video card': 'video card',
        'power supply': 'power supply',
        'thermal paste': 'thermal paste',
        'hdd': 'hdd',
        'ssd': 'ssd',
        'keyboard': 'keyboard',
        'laptop battery': 'laptop battery'
    }

    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            category_name = category.name.lower()
            if category_name in category_forms:
                form_class, form_type = category_forms[category_name]
                form_html = render_to_string('mainapp/form_template.html', {'form': form_class(), 'form_type': form_type}, request=request)
        except Category.DoesNotExist:
            pass

    if subcategory_id:
        try:
            subcategory = SubCategory.objects.get(id=subcategory_id)
            subcategory_name = subcategory.name.lower()
            if subcategory_name in subcategory_forms:
                form_type = subcategory_forms[subcategory_name]
                form_html = render_to_string('mainapp/form_template.html', {'form': PartsOrAccessoriesForm(), 'form_type': form_type}, request=request)
        except SubCategory.DoesNotExist:
            pass

    return JsonResponse({'form_html': form_html})

def success_page(request):
    return render(request, 'mainapp/success.html')
