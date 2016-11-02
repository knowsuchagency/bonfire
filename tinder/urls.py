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
                  'mentions_snapchat',
                  'mentions_kik',
                  'mentions_instagram',
                  'photos',
                  'instagram_photos',
                  )

class UserFilter(filters.FilterSet):


    def filter_snapchatters(self, queryset, name):
        print(queryset, name)
        return list(u for u in queryset if u.mentions_snapchat)

    mentions_snapchat = filters.BooleanFilter(method=filter_snapchatters)

    class Meta:
        model = User
        fields = ('name', 'age', 'distance', 'mentions_snapchat',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = UserFilter
    filter_fields = ('name', 'age', 'distance', 'mentions_snapchat',)



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]