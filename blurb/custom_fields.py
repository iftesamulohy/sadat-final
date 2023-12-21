import json
import requests
from django import forms

class ApiDataField(forms.CharField):
    def __init__(self, api_url, *args, **kwargs):
        self.api_url = api_url
        super().__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['data-api-url'] = self.api_url
        return attrs

    def get_suggestions(self, value):
        # Fetch data from the API based on the provided value
        response = requests.get(f"{self.api_url}?query={value}")
        data = response.json()
        return data.get('suggestions', [])

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['data-api-url'] = self.api_url
        return attrs
