from rest_framework.pagination import PageNumberPagination

from api.constants import PAGE_NUMBER


class CustomPageNumberPagination(PageNumberPagination):
    page_size = PAGE_NUMBER
    page_size_query_param = 'limit'
