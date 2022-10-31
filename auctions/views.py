from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
    items_on_watchlist=Item.objects.filter(watch=request.user.id)
    items_not_on_watchlist = Item.objects.exclude( watch=request.user.id)
    return render(request, "auctions/index.html",{
        "items": items_on_watchlist.filter(is_closed=False),
        "watch": items_not_on_watchlist.filter(is_closed=False),
        "title":"Active Listings",
    })

def user(request,user_id):
    items_on_watchlist=Item.objects.filter(watch=request.user.id)
    items_not_on_watchlist = Item.objects.exclude( watch=request.user.id)
    return render(request, "auctions/index.html",{
        "items": items_on_watchlist.filter(creator=user_id),
        "watch": items_not_on_watchlist.filter(creator=user_id),
        "title":"User Listings",
    })

def not_logged(request):
    return render(request, "auctions/login.html", {
        "message": "You need to be logged to perform this action."
    })
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def list_categories(request):
    return render(request, "auctions/list_categories.html",{
        "categories": Category.objects.all()
    })

def category(request,category):
    cat = Category.objects.get(pk=category)
    items_on_watchlist=Item.objects.filter(watch=request.user.id)
    items_not_on_watchlist = Item.objects.exclude( watch=request.user.id)
    return render(request, "auctions/index.html",{
        "items": items_on_watchlist.filter(category=category),
        "watch": items_not_on_watchlist.filter(category=category),
        "title": cat.title,
    })

def listing(request, listing_id):
    listing=Item.objects.get(pk=listing_id)
    bidders=[]

    for i in listing.bids.all():
        if i.bidder not in bidders:
            bidders.append(i.bidder)

    length=len(bidders)
    bid_ids = listing.bids.all().values('pk')
    max_bid=listing.start_price
    in_watchlist = request.user in listing.watch.all()
    max_bidder=None

    for bid_id in bid_ids:
        if Bid.objects.get(pk=bid_id['pk']).price>max_bid:
            max_bid=Bid.objects.get(pk=bid_id['pk']).price
            max_bidder = Bid.objects.get(pk=bid_id['pk']).bidder
    return render(request, "auctions/listing.html",{
        "item":listing,
        "title":listing.title,
        "price":max_bid,
        "bidders":length,
        "comments":Item.objects.get(pk=listing_id).comments.all(),
        "in_watchlist": in_watchlist,
        "bidder": max_bidder,
    })


def open_bidding(request, listing_id):
    listing=Item.objects.get(pk=listing_id)
    if request.user==listing.creator:
        listing.is_closed=False
        listing.save()
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))
    return HttpResponseRedirect(reverse("listing",args=[post,"You can't do that!"]))


def close_bidding(request, listing_id):
    listing=Item.objects.get(pk=listing_id)
    if request.user==listing.creator:
        listing.is_closed=True
        listing.save()
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))
    return HttpResponseRedirect(reverse("listing",args=[post,"You can't do that!"]))


def watchlist(request):
    if request.user.is_authenticated:
        items=Item.objects.filter(watch=request.user.pk)

        return render(request, "auctions/index.html",{
            "items": items,
            "watch": None,
            "title": "Watchlist",
            })
    return HttpResponseRedirect(reverse("login"))
def watchlist_add(request,id):
    listing=Item.objects.get(pk=id)
    listing.add_to_watchlist(request.user.pk)
    return redirect(request.META['HTTP_REFERER'])

def watchlist_remove(request,id):
    listing=Item.objects.get(pk=id)
    listing.remove_from_watchlist(request.user.pk)
    return redirect(request.META['HTTP_REFERER'])

def add_comment(request,listing_id):
    if request.user.is_authenticated:
        post = Item.objects.get(pk=listing_id)

        if request.method == "POST":
            text = request.POST["text"]
            user = request.user
            comment = Comment(text=text,user=user,post=post)
            comment.save()
    return redirect(request.META['HTTP_REFERER'])


def delete_comment(request,comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect(request.META['HTTP_REFERER'])


def place_bid(request, listing_id):
    if request.user.is_authenticated:
        item = Item.objects.get(pk=listing_id)
        user = request.user
        bid_ids = item.bids.all().values('pk')
        max_bid=item.start_price
        max_bidder= None
        bidders=[]
        in_watchlist = request.user in item.watch.all()

        for i in item.bids.all():
            if i.bidder not in bidders:
                bidders.append(i.bidder)

        length=len(bidders)
        for bid_id in bid_ids:
            if Bid.objects.get(pk=bid_id['pk']).price>max_bid:
                max_bid=Bid.objects.get(pk=bid_id['pk']).price
                max_bidder = Bid.objects.get(pk=bid_id['pk']).bidder

        if request.method == "POST":
            price = float(request.POST["bid"])

            if price>max_bid:
                bid = Bid( item=item,bidder=user,price=price)

                try:
                    bid.save()
                    max_bid=price
                    max_bidder = user
                    if user not in bidders:
                        length=length+1
                    return render(request, "auctions/listing.html",{
                        "item":item,
                        "title":item.title,
                        "price":"{:.2f}".format(max_bid),
                        "bidders":length,
                        "comments":Item.objects.get(pk=listing_id).comments.all(),
                        "in_watchlist": in_watchlist,
                        "bidder": max_bidder,
                        "message": "Successfully placed bid",
                        })
                except:
                    return render(request, "auctions/listing.html",{
                        "item":item,
                        "title":item.title,
                        "price":max_bid,
                        "bidders":length,
                        "comments":Item.objects.get(pk=listing_id).comments.all(),
                        "in_watchlist": in_watchlist,
                        "bidder": max_bidder,
                        "message": "Invalid bid",
                        })
            return render(request, "auctions/listing.html",{
                "item":item,
                "title":item.title,
                "price":max_bid,
                "bidders":length,
                "comments":Item.objects.get(pk=listing_id).comments.all(),
                "in_watchlist": in_watchlist,
                "bidder": max_bidder,
                "message": "Your bid must be larger than the existing",
            })
        return HttpResponseRedirect(reverse("listing",args=[listing_id]))

    else:
        return HttpResponseRedirect(reverse("not_logged"))

def new_listing (request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            description = request.POST["description"]
            price = request.POST["price"]

            if request.POST["category"] == "":
                category = None
            else:
                category = Category.objects.get(pk=request.POST["category"])

            try:
                image = request.FILES['image']
            except:
                image='items/default.jpg'

            creator = request.user
            listing=Item(title=title,description=description, start_price = price, category=category,image=image,creator=creator)
            listing.save()
            return HttpResponseRedirect(reverse("listing",args=[listing.pk]))

        return render(request, "auctions/new_listing.html",{
            'categories':Category.objects.all()
        })
    return HttpResponseRedirect(reverse("not_logged"))
