from django.urls import reverse_lazy
from .forms import SignUpForm, LoginForm, UserUpdateForm, AddCarForm, AddCarNumberForm, AddCarModelForm
from django.views.generic import TemplateView, FormView, RedirectView, UpdateView, CreateView, DetailView
from .models import User, CarNumber, Model, Car

from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Trip
from .serializers import LogInSerializer, NestedTripSerializer, UserSerializer


class MainPageView(TemplateView):
    template_name = 'core/main_page.html'


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NestedTripSerializer

    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            return Trip.objects.filter(
                Q(status=Trip.REQUESTED) | Q(driver=user)
            )
        if user.group == 'rider':
            return Trip.objects.filter(rider=user)
        return Trip.objects.none()


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'core/profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        kwargs['cars'] = Car.objects.filter(user=self.request.user)
        return super().get_context_data(**kwargs)


class ProfileDetailView(DetailView):
    model = User
    template_name = 'core/detail_profile.html'


class NumberUpdateView(CreateView):
    model = CarNumber
    form_class = AddCarNumberForm
    template_name = 'core/add_number.html'
    success_url = reverse_lazy('add_car')


class ModelUpdateView(CreateView):
    model = Model
    form_class = AddCarModelForm
    template_name = 'core/add_model.html'
    success_url = reverse_lazy('add_car')


class CarUpdateView(CreateView):
    model = Car
    fields = '__all__'
    template_name = 'core/add_car.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        User = form.save(self.request.user)
        return super().form_valid(User)
