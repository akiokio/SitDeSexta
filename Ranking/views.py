__author__ = 'AkiO'
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response,RequestContext
from django.http import HttpResponseRedirect
from Ranking.models import *
from Ranking.forms import *

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import redirect, get_object_or_404

def landing_page(request):
    news = News.objects.all().order_by('-pub_date')[:3]

    if request.user.is_authenticated():
        return HttpResponseRedirect('/index/')
    else:
        return render_to_response('landing_page.html',{
            'news': news,
            },context_instance=RequestContext(request))

@login_required()
def index(request):
    players = Player.objects.all()
    tournament = Tournament.objects.filter()
    profile = request.user.get_profile()

    return render_to_response('index.html',
        {'players': players,
         'tournaments':tournament,
          'profile':profile,
        }
        ,context_instance=RequestContext(request))

@login_required()
def tournaments(request):
    print request.user
    tournaments = Tournament.objects.filter(player__user__username=request.user)
    print tournaments

    return render_to_response('tournaments.html',
        {'tournaments':tournaments}
        ,context_instance=RequestContext(request)
    )

@login_required()
def tournament(request , tournament_id):
    tournament = Tournament.objects.filter(id=tournament_id)[0]

    return render_to_response('tournament.html',
        {'tournament': tournament}
        ,context_instance=RequestContext(request)
    )

@login_required()
def news(request, news_id):
    new = News.objects.filter(id=news_id)[0]

    return render_to_response('news.html',
        {'new':new}
        ,context_instance=RequestContext(request)
    )

def contato(request):

    if request.method == 'POST':
        form = formContato(request.POST)

        if form.is_valid():
            form.enviar()
            mostrar = 'Contato Enviado!'
    else:
        form = formContato()

    return render_to_response('contact.html',
        locals(),
        context_instance=RequestContext(request)
    )

@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required()
def profile(request):
    user = request.user.get_profile()

    return render_to_response('profile.html', {
        'user':user
    }, context_instance=RequestContext(request))