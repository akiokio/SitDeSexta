__author__ = 'AkiO'
# -*- coding: UTF-8 -*-

from django.contrib import admin
from models import Tournament, Player, Itm, News

class playerInline(admin.TabularInline):
    model = Tournament.player.through
    extra = 1

class itmInline(admin.TabularInline):
    model = Itm
    extra = 3

class tournamentAdmin(admin.ModelAdmin):
    inlines = (playerInline, itmInline,)
    exclude = ('player',)

admin.site.register(Tournament , tournamentAdmin)
admin.site.register(News)

