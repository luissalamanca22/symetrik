from rest_framework import mixins, status, viewsets, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from rest_framework.response import Response

from importer.models import DBModel


class ImportedTablesApiView(APIView):
    permission_classes = (AllowAny, )
    order_by_param = "order_by"
    page_param = "page"

    def get_filters(self):
        """
        Returns the filters be applied on the query and 
        removes the fields that are not for filtering
        """
        params = self.request.query_params.dict()
        if self.order_by_param in params:
            del params[self.order_by_param]
        if self.page_param in params:
            del params[self.page_param]
        return params

    def get_order_by(self):
        """Returns the field to order the records"""
        return self.request.query_params.get(self.order_by_param, None)

    def get_page(self):
        """Returns the field to limit the records"""
        return self.request.query_params.get(self.page_param, None)

    def get(self, request, tablename):
        try:
            query = DBModel.get_results(
                tablename, 
                filters=self.get_filters(),
                order_by=self.get_order_by(),
                page=self.get_page()
            )
            data = DBModel.serialize_results(query)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response(
                {"error": str(ex), "message": "There was an internal error."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
