from django.contrib import admin
from .custom_fields import ApiDataField
from blurb.models import Category, Image, Market, Prices, Products, Reviews, Slider, SliderItem, SubCategory, SubsubCategory
from django.db import models
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.urls import path  # Add this import
#here is the code
class ProductsAdminForm(forms.ModelForm):
    # Define the additional field(s)
    custom_input = forms.CharField(
        label='AI Assistant',
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 100}),
         required=False
    )

    class Meta:
        model = Products
        fields = '__all__'
# Register your models here.
@admin.register(SubsubCategory)
class SubsubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    list_display = ['title']
@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ['title']
@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['name']
@admin.register(Prices)
class PricesAdmin(admin.ModelAdmin):
    list_display = ['price']
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    form = ProductsAdminForm
    list_display = ['name']
    change_form_template = 'admin/change_form_custom_action.html'

    def custom_action(self, request, object_id):
        # Your custom logic here
        # For demonstration purposes, let's assume you want to print the name of the selected item
        selected_item = Products.objects.get(pk=object_id)
        print(f"Custom action performed for item: {selected_item.name}")

        self.message_user(request, "Custom action completed.")
        return super().change_view(request, object_id)

    custom_action.short_description = "Custom Action"
    
    
