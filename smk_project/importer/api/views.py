

class ComunaApiView(APIView):
    permission_classes = (AllowAny, IsAuthenticated)

    def get(self, request, municipio_pk):
        qs = Comuna.objects.filter(municipio=municipio_pk).all()
        return Response(ComunaSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ComunaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comuna = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

