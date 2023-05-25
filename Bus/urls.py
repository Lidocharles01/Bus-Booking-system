from django.urls import path
from .views import home,about_us,signin,signup,bus_payment,cancellings,signout,user_home,profile,view_profile,edit_profile,change_password,findbus,bookings,seebookings,seat_book
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('about-us', about_us, name="aboutus"),
    path('user_home', user_home, name="user_home"),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('signout/', signout, name="signout"),
    path('profile/', profile, name="profile"),
    path('view_profile/', view_profile, name="view_profile"),
    path('edit_profile/', edit_profile, name="edit_profile"),
    path('change_password/',change_password.as_view(), name="change_password"),
    path('findbus', findbus, name="findbus"),
    path('bookings', bookings, name="bookings"),
    path('seebookings', seebookings, name="seebookings"),
    path('cancellings', cancellings, name="cancellings"),
    path('seat_book', seat_book, name="seat_book"),
    path('bus_payment', bus_payment, name='bus_payment'),

    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
