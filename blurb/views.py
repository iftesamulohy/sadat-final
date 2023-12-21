from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.db.models import Prefetch
from django.contrib import messages  # Import the messages module
from blurb.models import Category, Image, Market, Prices, Products, Reviews
from rest_framework.decorators import api_view
from rest_framework.response import Response
import openai
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
# Create your views here.
class Index(TemplateView):
    template_name = "blurb/index-third-home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['categories'] = Category.objects.all()
        context['markets'] = Market.objects.all()
        print(context,"hello")
        
        # try:
        #     search_category = Keyword.objects.filter(user = self.request.user).last()
        #     context['recomends'] = Item.objects.filter(category__name=search_category.keyword,status='Free')
        # except:
        #     return context
        products_by_market = {}
        for market in context['markets']:
            products = Products.objects.filter(market=market).prefetch_related(
                Prefetch('product_image', queryset=Image.objects.all()),
                Prefetch('prices', queryset=Prices.objects.all()),
                Prefetch('reviews', queryset=Reviews.objects.all())
            )
            products_by_market[market.name] = products

        context['products_by_market'] = products_by_market
        print(context,"hiii")
        return context

class Conditions(TemplateView):
    template_name = "blurb/conditions.html"



class Shop(TemplateView):
    template_name = "blurb/shop-left-sidebar.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['products'] = Products.objects.all()
        return context
class ProductDetails(TemplateView):
    template_name = "blurb/product-details.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        product_slug = kwargs['slug']
        context['product'] = get_object_or_404(Products, slug=product_slug)
        return context
    def post(self, request, *args, **kwargs):
        # Handle form submission for posting reviews
        name = self.request.POST.get('name')
        email = self.request.POST.get('email')
        pros = self.request.POST.get('pros')
        cons = self.request.POST.get('cons')
        rating = self.request.POST.get('rating')
        p_id= self.request.POST.get('product_id')
        print("all data",name,email,pros,cons,rating,p_id)
        if name and email and pros and cons and rating:
            product = get_object_or_404(Products, id=p_id) 
            review = Reviews(name=name, email=email, pros=pros, cons=cons, rating=rating)
            review.save()
             # Add the review to the product's reviews
            product.reviews.add(review)
            messages.success(self.request, 'Review posted successfully.')
        else:
            messages.error(self.request, 'All fields are required.')

        # Redirect to the same page after form submission
        return HttpResponseRedirect(self.request.path_info)
class Wishlist(TemplateView):
    template_name = "blurb/wishlist.html"

class Error(TemplateView):
    template_name = "blurb/404.html"

class ChatAPIView(APIView):
    def get(self, request, *args, **kwargs):
        text = request.query_params.get('text', '')
        if text:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=text,
                temperature=0.7,
                max_tokens=150
            )['choices'][0]['text']
            return Response({'response': response})
        else:
            return Response({'error': 'Text parameter is required.'}, status=400)
