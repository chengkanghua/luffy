from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    # page_query_param = 'pp'
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 20


    #127.0.0.1:8001/?pp=3&size=10


