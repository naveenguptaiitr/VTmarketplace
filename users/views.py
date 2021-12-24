from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from actions.models import Action
from users.models import Details


# user profile controller
def profile(request, username):

    user1 = get_object_or_404(User, username=username)
    try:

        actions = Action.objects.filter(user=user1).order_by('-created')

    except Action.DoesNotExist:
        actions = None

    return render(request, "users/user/profile.html", {"user": user1, "actions": actions})


# create user account
def register(request):

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email,
                                        password=password)

        login_user(request)
        messages.add_message(request, messages.SUCCESS,
                             "Your account is successfully registered with the username: %s" % user.username)
        return redirect("marketplace:marketplace_home_page")

    return render(request,
                  "users/user/register.html")


# controller to login in the website
def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS, "You have logged in successfully.")
    else:
        messages.add_message(request, messages.ERROR, "Invalid username or password.")

    return redirect('marketplace:marketplace_home_page')


# controller to logout from the website
def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('marketplace:marketplace_home_page')


# controller to navigate to the edit item view
def profile_edit(request, username):
    all_users = User.objects.all()
    if "username" in request.session:
        for user in all_users:
            if user.username == username:
                break
        return render(request, "users/user/profile_edit.html", {"user_list": user})

    else:
        return redirect('marketplace:marketplace_home_page')


# controller to edit detail of an item
def edit_detail(request, username):
    user1 = User.objects.get(username=request.session.get("username"))
    user = User.objects.get(username=username)

    if request.method == 'POST':
        _firstname = request.POST.get("firstname")
        _lastname = request.POST.get("lastname")
        _email = request.POST.get("email")
        _profilepicture = request.POST.get("profile-picture")
        _gender = request.POST.get("gender")
        _password = request.POST.get("password")

        role = user.details.role
        if request.session['role'] == "admin":
            _role = request.POST.get("role")
            user.details.role = _role

        user.first_name = _firstname
        user.last_name = _lastname
        user.email = _email
        if _password:
            user.set_password(_password)
        user.details.gender = _gender


        if _profilepicture != "":
            user.details.profile_pic = "profilepicture/" + _profilepicture

        user.save()
        userID = User.objects.get(username=username).id
        userProfile = Details.objects.get(user_id=userID)

        # log the change role action
        if request.session['role'] == "admin" and role != _role:
            action = Action(
                user=user1,
                verb="Changed the user role to " + _role + " for ",
                target=userProfile
            )
            action.save()
        messages.add_message(request, messages.INFO,
                             "You have successfully edited your information")

        return redirect('users:profile', user.username)
    else:
        return redirect('users:profile', user.username)



