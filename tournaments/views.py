import json

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
import requests
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.urls import reverse

from tournaments.forms import JoinTournament, UserDetails, RegisterForm
from .models import TournamentJoin


def login_page(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.GET:
                return redirect(request.GET['next'])
            return redirect('tournaments:tournament_list', message=None)

    return render(request, 'tournaments/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('tournaments:tournament_list', message=None)


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('tournaments:login')

    return render(request, 'tournaments/register.html', {'form': form})


def tournament_list(request, message):
    url = 'http://127.0.0.1:8000/api/tournaments/'
    response = requests.get(url)
    tournaments = response.json()
    # print(tournaments)
    # print(message)
    if message != 'None':
        print('Not none')
        return render(request, 'tournaments/show_tournaments.html', {'tournaments': tournaments, 'msg': message})

    return render(request, 'tournaments/show_tournaments.html', {'tournaments': tournaments})


def tournament_list_util(request):
    return redirect('tournaments:tournament_list', message=None)


@login_required
def join_tournament(request, pk, t_name, start_date, end_date, location):
    form = JoinTournament()
    user_details_form = UserDetails(instance=request.user)
    if request.method == 'POST':
        form = JoinTournament(request.POST)
        user_details_form = UserDetails(request.POST, instance=request.user)
        if form.is_valid() and user_details_form.is_valid():
            url = 'http://127.0.0.1:8000/api/tournaments_join/'
            k = request.POST['pk']
            if TournamentJoin.objects.filter(user=request.user, tournament=k).exists():
                msg = 'You have already registered for this tournament'
                return redirect('tournaments:tournament_list', message=msg)
            name = user_details_form.cleaned_data['first_name']
            email = user_details_form.cleaned_data['email']
            phone_num = form.cleaned_data['phone_number']
            data = json.dumps({'name': name, 'tournament': k, 'mail': email, 'phoneNumber': phone_num})
            requests.post(url=url, data=data)

            t = TournamentJoin(user=request.user, name=name, email=email, tournament_name=t_name, start_date=start_date,
                               end_date=end_date, location=location, tournament=k)
            t.save()

            current_site = get_current_site(request)
            mail_subject = 'SportsHub Tournament Registration Confirmation'
            message = render_to_string('tournaments/activate_email.html', {
                'domain': current_site.domain,
                'user': name,
                'start_date': start_date,
                'end_date': end_date,
                'location': location,
                'tournament_name': t_name
            })
            email = EmailMessage(
                mail_subject, message, to=[email]
            )
            email.send()
            return redirect('tournaments:tournament_list', message="You have successfully joined the tournament")

        else:
            print('form is invalid')
            print(form.errors)

    print(int(pk))

    return render(request, 'tournaments/join_tournament.html', {'form': form, 'pk': int(pk),
                                                                'user_details_form': user_details_form})


@login_required
def user_tournament(request):
    tour_list = TournamentJoin.objects.filter(user=request.user)
    return render(request, 'tournaments/user_tournament.html', {'tournaments': tour_list})


@login_required
def leave_tournament(request, pk):
    if pk:
        try:
            instance = TournamentJoin.objects.get(user=request.user, tournament=pk)
            url = 'http://127.0.0.1:8000/api/tournament_leave/'
            data = json.dumps({'name': instance.name, 'tournament': pk})
            requests.post(url=url, data=data)
            instance.delete()
        except:
            pass

        return redirect('tournaments:user_tournament')
