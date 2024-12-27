from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "folders": data,
            "totalFolders": self.page.paginator.count,
            "currentPage": self.page.number,
            "totalPages": self.page.paginator.num_pages,
        })
