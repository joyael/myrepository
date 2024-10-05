"""
URL configuration for event_manage_proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from event_manage_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about', views.about),
    path('contact', views.contact),
    path('services', views.services),
    path('login', views.login),
    path('signup',views.signup),

    path('organizerlogin',views.organizerlogin),
    path('userlogin',views.userlogin),
    path('adminlogin',views.adminlogin),
    path('organizersignup',views.organizersignup,name='organizersignup'),
    path('usersignup',views.usersignup,name='usersignup'),
    path('userhome',views.userhome,name='userhome'),
    path('adminhome',views.adminhome),

    path('logout',views.logout,name='logout'),

    path('searchevent',views.searchevent,name='searchevent'),
    path('userevents',views.userevents,name='userevents'),
    path('userownevents', views.userownevents,name='userownevents'),
    path('createeventuser',views.createeventuser,name='createeventuser'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('edituserprofile',views.edituserprofile,name='edituserprofile'),
    path('singleevent/<int:d>', views.singleevent,name='singleevent'),
    path('canceleventuser/<int:d>', views.canceleventuser,name='canceleventuser'),
    path('bookevent/<int:d>', views.bookevent,name='bookevent'),
    path('payeventuser/<int:d>',views.payeventuser,name='payeventuser'),
    path('showusertickets',views.showusertickets,name='showusertickets'),
    path('cancelticket/<int:d>',views.cancelticket,name='cancelticket'),
    path('cancelticket2/<int:d>',views.cancelticket2,name='cancelticket2'),
    path('refundticket/<int:d>',views.refundticket,name='refundticket'),
    path('refundevent/<int:d>',views.refundevent,name='refundevent'),


    path('payment/<int:event_id>/<str:type>',views.single_razor,name='payment'),
    path('razorpaycheck/<int:price>',views.razorpaycheck,name='razorpaycheck'),
    path('success',views.success,name='success'),





    path('organizerhome', views.organizerhome,name='organizerhome'),
    path('organizerevents', views.organizerevents, name='organizerevents'),
    path('createeventorganizer', views.createeventorganizer, name='createeventorganizer'),
    path('payeventorganizer/<int:d>', views.payeventorganizer, name='payeventorganizer'),
    path('canceleventorganizer/<int:d>', views.canceleventorganizer,name='canceleventorganizer'),
    path('canceleventnopayorganizer/<int:d>', views.canceleventnopayorganizer,name='canceleventnopayorganizer'),
    path('organizerprofile', views.organizerprofile, name='organizerprofile'),
    path('editorganizerprofile', views.editorganizerprofile, name='editorganizerprofile'),
    path('createeventorganizer',views.createeventorganizer),
    path('singleeventorganizer/<int:d>',views.singleeventorganizer, name='singleeventorganizer'),


    path('eventcategories', views.eventcategories,name='eventcategories'),
    path('addeventcategory', views.addeventcategory,name='addeventcategory'),
    path('venues', views.venues,name='venues'),
    path('addvenue', views.addvenue,name='addvenue'),
    path('events',views.events,name='events'),
    path('vieworganizers',views.vieworganizers,name='vieworganizers'),

    path('approveevent/<int:d>', views.approveevent,name='approveevent'),
    path('disapproveevent/<int:d>', views.disapproveevent),
    path('rejectevent/<int:d>', views.rejectevent,name='rejectevent'),
    path('eventsbyvenue/<int:d>',views.eventsbyvenue, name='events_by_venue'),
    path('singleeventadmin/<int:d>',views.singleeventadmin, name='singleeventadmin'),

    path('forgot', views.forgot_password_user, name="forgot"),
    path('reset/<token>', views.reset_password_user, name='reset_password'),
    path('forgotorganizer', views.forgot_password_organizer, name="forgotorganizer"),
    path('resetorganizer/<token>', views.reset_password_organizer, name='resetorganizer'),

]



if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)