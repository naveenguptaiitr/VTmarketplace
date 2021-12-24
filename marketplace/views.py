from django.shortcuts import render, redirect
from datetime import datetime
from .models import MarketPlaceItemObject, CreateComment
from django.contrib import messages
from django.http import JsonResponse
from actions.models import Action
from users.models import Details
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime


# controller for the home view page
def marketplace_views_home(request):
    items = MarketPlaceItemObject.objects.all()

    try:
        actions = Action.objects.all().order_by('-created')

    except Action.DoesNotExist:
        actions = None
    return render(request,
                  "marketplace/views/home.html",
                  {"purchase_history": items, "sale_item": items, "new_listing": items, "actions": actions}
                  )


# controller for the list view page
def marketplace_views_list(request):
    electronic_item_detail_view = MarketPlaceItemObject.objects.order_by('id')
    return render(request,
                  "marketplace/views/list.html",
                  {"item_list": electronic_item_detail_view}
                  )


# controller for the detail view page
def detail(request, item_id):

    all_item = MarketPlaceItemObject.objects.all()

    all_comments = CreateComment.objects.filter(item_id=item_id)

    for item in all_item:
        if item.id == item_id:
            break

    return render(request,
                          "marketplace/views/detail.html",
                          {"item_detail": item, "recommendation_product": all_item, "item_comments": all_comments})


# controller to navigate to add an item
def add(request):

    if not request.session.get('username', False):
        return marketplace_views_home(request)

    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        product_description = request.POST.get("product_description")
        product_price = request.POST.get("product_price")
        img1 = "data/" + request.POST.get("item-img-1")
        img2 = "data/" + request.POST.get("item-img-2")
        img3 = "data/" + request.POST.get("item-img-3")
        img4 = "data/" + request.POST.get("item-img-4")

        user = User.objects.get(username=request.session.get("username"))

        item = MarketPlaceItemObject(
            prod_name=product_name,
            prod_price=product_price,
            prod_description=product_description,
            prod_type=product_category,
            prod_seller=user.username,
            user=user,
            date_posted=datetime.now(),
            img_path_1=img1,
            img_path_2=img2,
            img_path_3=img3,
            img_path_4=img4
        )

        item.save()

        # log the action
        action = Action(
            user=user,
            verb="added an item",
            target=item
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "You have successfully added the product: %s" % item.prod_name)
        return redirect('marketplace:marketplace_detail_item', item.id)
    else:
        return render(request, "marketplace/views/add.html")


# controller to navigate to the edit item view
def edit(request, item_id):
    all_item = MarketPlaceItemObject.objects.all()
    if "username" in request.session:
        for items in all_item:
            if items.id == item_id:
                break
        return render(request, "marketplace/views/edit.html", {"item_list": items})

    else:
        return marketplace_views_home(request)


# controller to edit detail of an item
def edit_item(request, item_id):

    item = MarketPlaceItemObject.objects.get(pk=item_id)
    user = User.objects.get(username=request.session.get("username"))

    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        product_category = request.POST.get("product_category")
        product_description = request.POST.get("product_description")
        product_price = request.POST.get("product_price")

        if item.prod_name != product_name:
            verb = "edited the item name to "
        elif item.prod_description != product_description:
            verb = "edited the item description to "
        else:
            verb = "edited the item detail to "

        item.prod_name = product_name
        item.prod_type = product_category
        item.prod_description = product_description
        item.prod_price = product_price
        item.save()

        # log the action
        action = Action(
            user=user,
            verb=verb,
            target=item
        )
        action.save()

        messages.add_message(request, messages.INFO,
                             "You have successfully edited the product: %s" % item.prod_name)

        return redirect('marketplace:marketplace_detail_item', item_id)
    else:
        return render(request, "marketplace/views/edit.html", {"item_list": item})


# controller to navigate to the delete an item view
def delete(request, item_id):

    item = MarketPlaceItemObject.objects.get(pk=item_id)

    if request.session['username'] == item.user.username or request.session['role'] == 'admin':

        return render(request, "marketplace/views/delete.html", {"item_list": item})

    else:
        return redirect('marketplace:marketplace_home_page')


# controller to delete an item from the list
def delete_item(request):

    if request.method == 'POST':
        item_id = request.POST.get("id")
        confirmation = request.POST.get("confirmation")
        if confirmation == 'yes':
            item = MarketPlaceItemObject.objects.get(pk=item_id)
            item_name = item.prod_name
            item.delete()

            action = Action(
                user=User.objects.get(username=request.session.get("username")),
                verb="deleted an item " + item_name,
                target=item
            )
            action.save()
            messages.add_message(request, messages.WARNING,
                                 "You have successfully deleted the product: %s" % item_name)

        return redirect('marketplace:marketplace_list_items')


# search result
def search_result(request):

    return render(request, "marketplace/views/search.html")


# Post comment
def add_comment(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    _newCommentList=[]
    if is_ajax and request.method == 'POST':
        _comment = request.POST.get('_comment')
        _username = request.session.get("username")
        try:
            _newComment = CreateComment(
                 comment=_comment,
                 user_id=User.objects.get(username=_username).id,
                 item_id=item_id
            )
            _newComment.save()

            action = Action(
                user=User.objects.get(username=_username),
                verb="added a new comment",
                target=_newComment
            )
            action.save()
            _newCommentList.append({"id": _newComment.id, "comment": _newComment.comment,
                                    "date": naturaltime(_newComment.created), "user": _newComment.user.username})

            return JsonResponse({'success': 'success', 'comments': _newCommentList}, status=200)
        except MarketPlaceItemObject.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)


# read comment using ajax
def read_comment(request, item_id):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET':
        try:
            if "username" in request.session:
                userID = User.objects.get(username=request.session.get("username")).id
                userRole = Details.objects.get(user_id=userID)
                role = userRole.role
            else:
                role = None

            com_object = CreateComment.objects.filter(item_id=item_id).order_by('-created')
            _comment_list = []

            for record in com_object:
                _comment_list.append({"id": record.id, "comment": record.comment,
                                      "date": naturaltime(record.created), "user": record.user.username, "role": role})

            return JsonResponse({'success': 'success', 'comments': _comment_list}, status=200)

        except CreateComment.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)


def edit_comment_page(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        comment_id = request.POST.get('_comment_id')
        updated_comment = request.POST.get('_new_comment')
        try:
            comment = CreateComment.objects.get(pk=comment_id)
            comment.comment = updated_comment
            comment.save()

            return JsonResponse({'success': 'success'}, status=200)
        except MarketPlaceItemObject.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)


# delete comment
def delete_comment(request):

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        comment_id = request.POST.get('_comment_id')
        try:
            comment = CreateComment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({'success': 'success'}, status=200)
        except MarketPlaceItemObject.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid AJAX request'}, status=400)


def sort_by_item(request):
    items = MarketPlaceItemObject.objects.order_by('prod_name')
    return render(request,
                  "marketplace/views/list.html",
                  {"item_list": items}
                  )



# Non-Ajax comment implementation
# def comment(request, item_id):
#
#     if request.method == 'POST':
#         _comment = request.POST.get('user_new_comment')
#         _username = request.session.get("username")
#
#         _newComment = CreateComment(
#             comment=_comment,
#             user_id=User.objects.get(username=_username).id,
#             item_id=item_id
#         )
#         _newComment.save()
#
#     return redirect('marketplace:marketplace_detail_item', item_id)
