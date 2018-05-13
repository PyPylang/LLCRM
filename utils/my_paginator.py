from utils.CustomPaginator import CustomPaginator, Paginator
from django.core.paginator import EmptyPage, PageNotAnInteger


# 传入字符型的当前页和分类数据列表

def my_paginator(request, posts_list):
    current_page = request.GET.get('_P')
    if current_page:
        current_page = int(current_page.strip())
    else:
        current_page = 1
    paginator = CustomPaginator(current_page, 5, posts_list, 4)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(Paginator.num_pages)
    return posts
