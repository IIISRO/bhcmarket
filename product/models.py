from django.db import models

# Create your models here.

from core.models import AbstractModel
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from slugify import slugify
from core.models import AbstractModel







class Category(MPTTModel):
    STATUS = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
        ('New', 'New')
    )
    parent = TreeForeignKey('self',blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10, default='New', choices=STATUS)
    detail = RichTextUploadingField(blank=True, null=True)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(blank=True,upload_to='CategoriesImages/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    def get_absolute_url(self):
        if self.parent:
            categories = []
            categories.append(self.slug)
            categories.append(self.parent.slug)
            if self.parent.parent:
                most_parent = self.parent.parent
                categories.append(most_parent.slug)
                while True:
                    if most_parent.parent:
                        most_parent = most_parent.parent
                        categories.append(most_parent.slug)
                    else:
                        break
            return f"{'/'.join(categories[::-1])}"
        else:
            return f'{self.slug}'  
        
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        self.title = self.title.capitalize()
        super(Category, self).save(*args, **kwargs)

   

    
    def get_childs(self):
        children = self.children.all()
        
        child_categories = []
        for child in children:
            child_categories.append(child)
            child_categories.extend(child.get_childs())
        
        return child_categories




class Product(AbstractModel):
    STATUS = (
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
        ('New', 'New')
    )
    title = models.CharField(max_length=150)
    price = models.FloatField(null=False, blank=False)
    category = models.ForeignKey('Category',related_name='category_products', on_delete=models.CASCADE, null=False, blank=False)
    status=models.CharField(max_length=50,default='New', choices=STATUS)
    description = models.TextField(max_length=255)
    detail = RichTextUploadingField()
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title

    
    def save(self,*args, **kwargs):
       
        self.slug = slugify(self.title)

        super(Product, self).save(*args, **kwargs)


    # method to create a fake table field in read only mode
    def image_tag(self):
        if Image.objects.filter(product = self).filter(is_main = True).exists():
            return mark_safe('<img src="{}" height="50"/>'.format(Image.objects.filter(product = self).filter(is_main = True).first().image.url))

        else:
            return mark_safe('<img src="" alt="no img" height="50"/>')

    def get_absolute_url(self):
        return f'{self.category.get_absolute_url()}/{self.slug}'

    def get_img(self):
        images = Image.objects.filter(product = self).filter(is_main = True)
        if images.exists():
            return images.first().image.url

    # order sayin tapmaga metodlar

class Image(AbstractModel):
    product=models.ForeignKey('Product', null=False, blank=False, on_delete=models.CASCADE)
    image = models.ImageField(blank=False, upload_to='ProductImages/')
    is_main = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Images"

    def __str__(self):
        return f'{self.product.title}|IMG'
