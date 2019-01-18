from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(user=user)

    def perform_create(self, serializer):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        serializer.save(ip=ip, user=self.request.user)


