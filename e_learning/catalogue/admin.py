from django.contrib import admin
from .models import Course, Category
from .pricing.models import Campaign, ProductSegment, UserSegment

admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Campaign)
admin.site.register(ProductSegment)
admin.site.register(UserSegment)
