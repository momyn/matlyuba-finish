from django.core import validators
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel






class Lookbook(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    image = models.ImageField('Картинка', upload_to='product/%Y/%m/%d', blank=True)

    def __str__(self):
        return self.name

class Look(models.Model):
    category = models.ForeignKey(Lookbook, on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='product/%Y/%m/%d', blank=True)
    slug = models.CharField('Ссылка', max_length=150, db_index=True, unique=True)
    available = models.BooleanField(default=True)

    def complete_update(self):


        self.status = 'Complete'
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    menu = models.BooleanField(default=False, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcategory')

    def children(self):
        """Return replies of a comment."""
        return Category.objects.filter(parent=self, menu=1)

    @property
    def is_parent(self):
        """Return `True` if instance is a parent."""
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return self.title


class CategoryManager(models.Manager):
    def all(self):
        """Return results of instance with no parent (not a reply)."""
        qs = super().filter(parent=None)
        return qs


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=1, related_name='category')


# class Category(MPTTModel):
# #     name = models.CharField(max_length=100, db_index=True)
# #     slug = models.SlugField(max_length=100, unique=True)
# #     parent = TreeForeignKey('self', on_delete=models.CASCADE, verbose_name=u'Родительская категория',
# #                             related_name='children', blank=True, null=True)
# #
# #     class Meta:
# #         unique_together = ('parent',)
# #         ordering = ('name', 'parent_id',)
# #         verbose_name = 'Категория'
# #         verbose_name_plural = 'Категории'
# #
# #     class MPTTMeta:
# #
# #             order_insertion_by = ['name']
# #
# #     def __str__(self):
# #         return self.name
# #
# #     def __unicode__(self):
# #         p_list = self._recurse_for_parents(self)
# #         p_list.append(self.name)
# #         return self.get_separator().join(p_list)
# #
# #     def _recurse_for_parents(self, cat_obj):
# #         p_list = []
# #         if cat_obj.parent_id:
# #             p = cat_obj.parent
# #             p_list.append(p.name)
# #             more = self._recurse_for_parents(p)
# #             p_list.extend(more)
# #         if cat_obj == self and p_list:
# #             p_list.reverse()
# #         return p_list
# #
# #     def get_separator(self):
# #         return ' :: '
# #
# #     def _parents_repr(self):
# #         p_list = self._recurse_for_parents(self)
# #         return self.get_separator().join(p_list)
# #
# #     _parents_repr.short_description = 'Category parents'
# #
# #     def save(self):
# #         p_list = self._recurse_for_parents(self)
# #         if self.name in p_list:
# #             raise validators.ValidationError('You must not save a category in itself')
# #         super(Category, self).save()
# #
# #
# #     def get_absolute_url(self):
# #         return reverse('product_list_by_category', args=[self.slug])
#
#
# # class Size(models.Model):
# #     name = models.CharField(max_length=24,)
# #
# #     def __str__(self):
# #         return str(self.name)




class Product(models.Model):
    STATUSES_CHOICES = (
        ('New', 'NEW'),
        ('Sold OUT', 'SOLD OUT'),
        ('coming soon', 'COMING SOON'),
        ('Bestseller', 'BESTSELLER'),
    )
    CHOOSE_SIZE = (
        ('Extra Small', 'XS'),
        ('Small', 'S'),
        ('Medium', 'M'),
        ('Large', 'L'),
        ('Extra Large', 'XL'),
        ('Double Large', 'XXL'),
        ('Triple Large', 'XXXL'),
    )

    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=25, choices=STATUSES_CHOICES)
    name = models.CharField('Имя', max_length=150, db_index=True)
    slug = models.CharField('Ссылка', max_length=150, db_index=True, unique=True)
    image = models.ImageField('Первая картинка', upload_to='product/%Y/%m/%d', blank=True)
    item_image_2 = models.ImageField('Вторая картинка', upload_to="product/%Y/%m/%d", null=False)
    item_image_3 = models.ImageField('Третья картинка', upload_to="product/%Y/%m/%d", null=False)
    description = models.TextField('Описания', max_length=1000, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    sku = models.CharField(("Артикул"), max_length=255, blank=True, null=True,
                           help_text=("Если оставить поле пустым, по умолчанию используется ярлык"))
    available = models.BooleanField('Доступный', default=True)
    created = models.DateTimeField('Создано', auto_now_add=True)
    uploaded = models.DateTimeField('Обновлено',auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])

    def complete_update(self):
        self.status = 'Complete'
        self.save()




class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(active=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colors(self):
        return self.all().filter(category='color')


VAR_CATEGORIES = (
    ('size', 'size',),
    ('color', 'color',),
    ('package', 'package'),
)


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=120, choices=VAR_CATEGORIES, default='size')
    title = models.CharField(max_length=120)
    image = models.ImageField(null=True, blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=100, null=True, blank=True)
    objects = VariationManager()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# Create your models here.
