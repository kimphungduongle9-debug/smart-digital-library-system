from rest_framework.pagination import PageNumberPagination


class DocumentPaginator(PageNumberPagination):
    page_size = 20