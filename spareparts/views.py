from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import SparePart, SparePartCategory


class SparePartListView(ListView):
    """
    Displays a paginated list of all spare parts.
    Supports ordering by newest first.
    """
    model = SparePart
    template_name = "spareparts/sparepart_list.html"
    context_object_name = "spare_parts"
    paginate_by = 12
    ordering = ['-created_at']


class SparePartDetailView(DetailView):
    """
    Displays detailed information about a single spare part,
    including dealer, category, images, and description.
    """
    model = SparePart
    template_name = "spareparts/sparepart_detail.html"
    context_object_name = "spare_part"

    def get_object(self, queryset=None):
        """
        Retrieves the SparePart instance based on the slug.
        """
        return get_object_or_404(SparePart, slug=self.kwargs.get('slug'))


class SparePartCategoryListView(ListView):
    """
    Displays a list of all spare part categories.
    """
    model = SparePartCategory
    template_name = "spareparts/category_list.html"
    context_object_name = "categories"
    ordering = ['name']


class SparePartCategoryDetailView(DetailView):
    """
    Displays detailed information about a category,
    including all spare parts under that category.
    """
    model = SparePartCategory
    template_name = "spareparts/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        """
        Adds all spare parts of this category to the template context.
        """
        context = super().get_context_data(**kwargs)
        context['spare_parts'] = self.object.spare_parts.all()
        return context
