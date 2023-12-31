from django.shortcuts import render
from django.views.generic import View, DetailView
from .models import Product, Category, Image
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.


class ProductsList(View):
    def get(self, request, category_path):
        slug = category_path.split('/')[-1]

        if category_path == 'all':
            context = {
                'slug':'All',
                'categories' : Category.objects.filter(parent = None).filter(Q(status="Active") | Q(status='New')),
                'products' : Product.objects.filter(Q(status="Active") | Q(status='New'))
                       
            }         

        else:
            category = Category.objects.filter(slug = slug).filter(parent = None).filter(Q(status="Active") | Q(status='New')).first()
            
            if not category or not category.get_absolute_url() == f'{category_path}':
                raise Http404
            
            category_childs = category.get_childs()
        
            if not category_childs:
                products = Product.objects.filter(category = category).filter(Q(status="Active") | Q(status='New'))
            else:
                products = Product.objects.filter(category = category).filter(Q(status="Active") | Q(status='New'))
                for child_cat in category_childs:
                    products = products.union(Product.objects.filter(category = child_cat).filter(Q(status="Active") | Q(status='New')))
            
            context = {
                'slug': category.title.capitalize(),
                'products': products,
                'child_categories' : Category.objects.filter(parent = category).filter(Q(status="Active") | Q(status='New'))
                       
            }         

        
        return render(request, 'products-list.html', context)
    
class ProductDetail(View):
     def get(self, request, category_path, slug):
        product = get_object_or_404(Product, slug = slug)
        if product.get_absolute_url() != f'{category_path}/{slug}' or product.status == 'Deactive':
            raise Http404
        context = {
            'product':product,
            'prod_detail_cats': category_path.replace('/', ', ').title(),
            'images': Image.objects.filter(product = product).order_by('-is_main')
        }
        return render(request, 'product-detail.html', context)