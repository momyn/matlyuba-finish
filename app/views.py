from itertools import product

from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from .models import Category, Product, Post, Lookbook, Look
from cart.forms import CartAddProductForm


from django.template import loader, Context, RequestContext



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'app/index.html',
                  {
                      "category": category,
                      "categories": categories,
                      "product": products
                  })


def category_page(request, category_id, render_to_response=None):
    #getting detail information about current object
    current_category = Category.objects.get(id=category_id)
    categories = Category.objects.filter(parent__isnull=True)
    root_category_id = current_category.get_root().id
    #render
    return render_to_response("app/shop.html",
                          {
                              'nodes':Category.objects.all(),
                              'current_category':current_category,
                              'root_category_id':root_category_id,
                              'categories': categories
                          },
                          context_instance=RequestContext(request))



def products(request, category_slug=None, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(parent__isnull=True)
    slug = category_slug
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'app/shop.html', {"product": products, "slug": slug, "categories": categories,})



def category_post(request, cslug ):
    posts = Post.objects.filter(category__slug=cslug)
    category = Category.objects.get(slug=cslug)
    context = {
        'category': category,
        'posts': posts,
    }

    return render(request, 'app/shop.html', context)

# def product_detail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug, available=True)
#     cart_product_form = CartAddProductForm()
#     return render(request, 'app/product/detail.html', {'product': product, 'cart_product_form': cart_product_form})


def product_detail(request, id, slug):
    products = Product.objects.filter(available=True)
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'app/product.html', {'product': product, 'cart_product_form': cart_product_form, 'products': products})




def about(request,):
    return render(request, 'app/about.html',)


def contact(request,):
    return render(request, 'app/contact.html',)



def lookbook(request,):
    title = Lookbook.objects.filter()
    return render(request, 'app/lookbook.html',
                  {'title': title})


def look(request, slug):
    image = Look.objects.filter(category__slug=slug)
    # look = Look.objects.filter()
    return render(request, 'app/look.html',
                  {'image': image, 'look': look })







# def product_list(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.objects.filter()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request,
#                   'app/index.html', {"product": products, "category": categories})
#
#
# def category_list(request, category_slug=None):
#     category = None
#     parents = Category.objects.get(id=1)
#     categories = Category.objects.filter()
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request,
#                   'app/shop.html', {"product": products, "parent": parents, "category": categories})
#
#
# def product(request, category_slug=None):
#     products = Product.objects.filter(available=True)
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request,
#                   'app/product.html', {"product": products})
#
#
# def product_detail(request, id, slug):
#     product = get_object_or_404(Product,
#                                 id=id,
#                                 slug=slug,
#                                 available=True)
#     return render(request,
#                   'app/product/detail.html',
#                   dict(product=product))
