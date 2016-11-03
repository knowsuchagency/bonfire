from django.conf.urls import url, include
from tinder import views
from tinder.models import User
from rest_framework import routers, serializers, viewsets, filters
from django_filters import rest_framework as filters

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name',
                  'age',
                  'distance',
                  'bio',
                  'instagram_username',
                  'snapchat_in_bio',
                  'instagram_in_bio',
                  'kik_in_bio',
                  'photos',
                  'instagram_photos',
                  )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = UserFilter
    filter_fields = ('name', 'age', 'distance', 'snapchat_in_bio',)



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]