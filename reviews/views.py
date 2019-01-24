from django.contrib.auth import get_user_model
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from reviews.models import Review
from reviews.serializers import ReviewSerializer, UserRegistrationSerializer


class ReviewsViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    list:
    Return a list of reviews posted by the user owning the access token.
    create:
    Endpoint for reviews posting. The reviews are being assigned to the user which post them and only he/she can see them
    """
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)
    perms = IsAuthenticated()

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(user=user)

    def perform_create(self, serializer):
        # In docker swarm mode this IP could be the the docker proxy IP.
        # Unfortunately, there is no solution at the moment by Docker, just a workaround, i.e. running in `host` network
        # which under MacOS is not working good. Under Linux distributions it should be fine, as well as in Kubernetes, Clouds, etc
        # see issue: https://github.com/moby/moby/issues/25526
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip=ip, user=self.request.user)


class RegisterView(mixins.CreateModelMixin, GenericViewSet):
    """
    create:
    A json encoded user details for user registration. Once posted if it is valid a new user will be created
    """
    serializer_class = UserRegistrationSerializer
    queryset = get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        resp.data = {}
        return resp
