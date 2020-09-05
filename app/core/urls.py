from django.urls import path
from app.core.views import TripView, MainPageView, ProfileUpdateView, NumberUpdateView, CarUpdateView, ModelUpdateView, ProfileDetailView

urlpatterns = [
    # path('signup/', MyRegisterFormView.as_view(), name="register"),
    # path('login/', LoginView.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='detail_profile'),
    path('profile/', ProfileUpdateView.as_view(), name="profile"),
    path('add/car/car_number', NumberUpdateView.as_view(), name='add_number'),
    path('add/car/car_model', ModelUpdateView.as_view(), name='add_model'),
    path('add/car', CarUpdateView.as_view(), name='add_car'),
    path('', MainPageView.as_view(), name='home'),
    path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
]
