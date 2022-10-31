from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("not_logged", views.not_logged, name="not_logged"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist/remove/<int:id>", views.watchlist_remove, name="watchlist_remove"),
    path("categories", views.list_categories, name="list_categories"),
    path("<str:category>", views.category, name="category"),
    path("user/<int:user_id>", views.user, name="user"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.place_bid, name = "place_bid"),
    path("listing/<int:listing_id>/comment", views.add_comment, name="add_comment"),
    path("listing/<int:comment_id>/delete_comment", views.delete_comment, name="delete_comment"),
    path("listing/<int:listing_id>/open_bidding", views.open_bidding, name="open_bidding"),
    path("listing/<int:listing_id>/close_bidding", views.close_bidding, name="close_bidding"),
    path("create/", views.new_listing, name="new_listing"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
