from django.contrib import admin
from django.urls import include, path, re_path

from web3_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path(
        r'^cryptkeeper/',
        include(
            'governance.urls',
            namespace='crypt_keepers'
        )
    ),
    re_path(
        r'^total-supply-tcap/$',
        views.TotalSupplyTCAP.as_view(),
        name='total-supply-tcap'
    ),
    re_path(
        r'^total-supply-ctx/$',
        views.TotalSupplyCTX.as_view(),
        name='total-supply-ctx'
    ),
    re_path(
        r'^total-crypto-market-cap/$',
        views.TotalMarketCap.as_view(),
        name='total-crypto-market-cap'
    ),
    re_path(
        r'^tcap-oracle-price/$',
        views.TcapOraclePrice.as_view(),
        name='tcap-oracle-price'
    ),
    re_path(
        r'^tcap-market-price/$',
        views.TcapMarketPrice.as_view(),
        name='tcap-market-price'
    ),
]

urlpatterns += static(settings.MEDIA_URL,
                    document_root=settings.MEDIA_ROOT)