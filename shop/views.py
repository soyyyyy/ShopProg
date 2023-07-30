from django.shortcuts import render, redirect
from .models import Item, Category, Tag, Comment, Manufacturer
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets
from .serializers import itemSerializer


class itemViewset(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = itemSerializer

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    item = comment.item
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(item.get_absolute_url())
    else:
        PermissionDenied


class ItemUpdate(LoginRequiredMixin, UpdateView):
    model = Item
    fields = ['name', 'hook_text', 'content', 'head_image', 'price', 'sensitivity', 'manufacturer', 'category']

    template_name = 'shop/item_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return super(ItemUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(ItemUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')
            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count
        return context


class ItemCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Item
    fields = ['name', 'hook_text', 'content', 'head_image', 'price', 'sensitivity', 'manufacturer', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            form.instance.author = current_user
            response = super(ItemCreate, self).form_valid(form)
            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')
                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response
        else:
            return redirect('/shop/')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count
        return context


class ItemList(ListView):
    model = Item
    ordering = '-pk'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count
        return context


class ItemSearch(ItemList):
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        item_list = Item.objects.filter(
            Q(name__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return item_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search : {q} ({self.get_queryset().count()})'
        return context


class ItemDetail(DetailView):
    model = Item

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ItemDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_item_count'] = Item.objects.filter(category=None).count
        context['manufacturers'] = Manufacturer.objects.all()
        context['no_manufacturer_item_count'] = Item.objects.filter(manufacturer=None).count
        context['comment_form'] = CommentForm
        return context



def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        item_list = Item.objects.filter(category=None)

    else:
        category = Category.objects.get(slug=slug)
        item_list = Item.objects.filter(category=category)

    return render(request, 'shop/item_list.html', {
        'category': category,
        'item_list': item_list,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
        'manufacturers': Manufacturer.objects.all(),
        'no_manufacturer_item_count': Item.objects.filter(manufacturer=None).count
    })

def manufacturer_page(request, slug):
    if slug == 'no_manufacturer':
        manufacturer = '미분류'
        item_list = Item.objects.filter(manufacturer=None)
    else:
        manufacturer = Manufacturer.objects.get(slug=slug)
        item_list = Item.objects.filter(manufacturer=manufacturer)
    return render(request, 'shop/item_list.html', {
        'manufacturer': manufacturer,
        'item_list': item_list,
        'manufacturers': Manufacturer.objects.all(),
        'no_manufacturer_item_count': Item.objects.filter(manufacturer=None).count,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
    })


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    item_list = tag.item_set.all()
    return render(request, 'shop/item_list.html', {
        'tag': tag,
        'item_list': item_list,
        'categories': Category.objects.all(),
        'no_category_item_count': Item.objects.filter(category=None).count,
        'manufacturers': Manufacturer.objects.all(),
        'no_manufacturer_item_count': Item.objects.filter(manufacturer=None).count
    })


def new_comment(request, pk):
    if request.user.is_authenticated:
        item = get_object_or_404(Item, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.item = item
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(item.get_absolute_url())
    else:
        raise PermissionDenied

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied




