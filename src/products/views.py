from django.shortcuts import render, get_object_or_404, Http404
from django.views.generic import ListView, DetailView
from .models import Product
from carts.models import Cart

# Create your views here.
class ProductListView(ListView):
  template_name = 'products/list.html'

  # def get_context_data(self, *args, **kwargs):
  #   context = super(ProductListView, self).get_context_data(*args, **kwargs)
  #   return context

  def get_context_data(self, *args, **kwargs):
    context = super(ProductListView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_queryset(self, *args, **kwargs):
    return Product.objects.all()

   
def product_listview(request): 
  queryset = Product.objects.all()
  context = {
    'object_list': queryset
  }
  return render(request,'products/list.html',context)

class ProductDetailSlugView(DetailView):
  template_name = 'products/detail.html'

  def get_queryset(self, *args, **kwargs):
    return Product.objects.all()

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
    cart_obj, new_obj = Cart.objects.new_or_get(self.request)
    context['cart'] = cart_obj
    return context

  def get_object(self, *args, **kwargs):
    request = self.request
    slug = self.kwargs.get('slug')
    #instance = get_object_or_404(Product, slug=slug, active=True)
    try:
        instance = Product.objects.get(slug=slug, active=True)
    except Product.DoesNotExist:
        raise Http404("Not found..")
    except Product.MultipleObjectsReturned:
        qs = Product.objects.filter(slug=slug, active=True)
        instance = qs.first()
    except:
        raise Http404("Uhhmmm ")
    return instance

class ProductDetailView(DetailView):
  template_name = 'products/detail.html'

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    return context
  
  # def get_queryset(self, *args, **kwargs):
  #   pk = self.kwargs.get('pk')
  #   return Product.objects.filter(pk=pk)
  
  def get_object(self, *args, **kwargs):
    request = self.request
    pk = self.kwargs.get('pk')
    instance = Product.objects.get_by_id(id=pk)

    if instance is None:
      raise Http404('Product doesnt exist')

    return instance

def product_detailview(request, pk = None, *args ,**kwargs ): 
  # instance = Product.objects.get(pk = pk, featured=True)
  # instance = get_object_or_404(Product, pk = pk, featured=True)
  # try:
  #   instance = Product.objects.get(id=pk)
  # except Product.DoesNotExist:
  #   print('no product here')
  #   raise Http404('Product doesnt exist')
  instance = Product.objects.get_by_id(id=pk)

  if instance is None:
    raise Http404('Product doesnt exist')

  context = {
    'object' : instance
  }
  return render(request,'products/detail.html',context)

class ProductFeaturedListView(ListView):
  template_name = 'products/list.html'

  # def get_context_data(self, *args, **kwargs):
  #   context = super(ProductListView, self).get_context_data(*args, **kwargs)
  #   return context

  def get_queryset(self, *args, **kwargs):
    request = self.request
    return Product.objects.all().featured()

class ProductFeaturedDetailView(DetailView):
  queryset = Product.objects.featured()
  template_name = 'products/featured-detail.html'

  def get_queryset(self, *args, **kwargs):
    return Product.objects.featured()
