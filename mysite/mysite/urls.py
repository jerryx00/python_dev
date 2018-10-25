"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.urls import include
import debug_toolbar

from learn import views as learn_views  # new


urlpatterns = [
    path('', learn_views.index),  # new
    path('add/', learn_views.add, name='add'),  # new
    path('add/<int:a>/<int:b>/', learn_views.add2, name='add2'),  # new
    path('view/', learn_views.view, name='view'),  # new
    path('admin/', admin.site.urls),
    path(r'^accounts/', include('users.urls')),

    # For django versions before 2.0:
    path('__debug__/', include(debug_toolbar.urls)),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
