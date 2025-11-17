from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

@api_view(["GET"])
def accounts_root(request):
    return Response({
        "register": "/api/accounts/register/",
        "me": "/api/accounts/me/",
    })
