from django.conf.urls import url, include
from tinder import views
from tinder.models import User
from rest_framework import routers, serializers, viewsets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name',
                  'age',
                  'photos',
                  'instagram_username',
                  'mentions_snapchat',
                  'mentions_kik',
                  'mentions_instagram',
                  'liked',
                  'tinder_id',
                  # 'data',
                  )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]