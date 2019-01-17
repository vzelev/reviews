from rest_framework import viewsets

from reviews.models import Review
from reviews.serializers import ReviewSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Review.objects.all()
        return Review.objects.filter(user=user)


