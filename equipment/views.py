import json

from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import MachineSerializer, ToolSerializer, FileUploadSerializer


# Create your views here.

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

class ToolViewSet(viewsets.ModelViewSet):
    queryset = Tool.objects.all()
    serializer_class = ToolSerializer









class BaseUploadView(APIView):
    parser_classes = (MultiPartParser,)
    def parse_file(self, request):
        file = request.data.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = json.loads(file.read())
            return data if isinstance(data, list) else [data]
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON file'}, status=status.HTTP_400_BAD_REQUEST)


class MachineUploadView(BaseUploadView):
    serializer_class = FileUploadSerializer
    def post(self, request):
        try:
            data = self.parse_file(request)
            serializer = MachineSerializer(data=data, many=isinstance(data, list))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ToolUploadView(BaseUploadView):
    serializer_class = FileUploadSerializer
    def post(self, request):
        try:
            data = self.parse_file(request)
            serializer = ToolSerializer(data=data, many=isinstance(data, list))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

