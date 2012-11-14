__author__ = 'AkiO'
# -*- coding: UTF-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from userena.models import UserenaBaseProfile
from django.utils.translation import ugettext as _

class Player(UserenaBaseProfile):
    '''
        Jogador de porker que participa de torneio
        relacionamento com ITM de 1 pra N
        relacionamento N pra N com torneio
    '''
    user = models.OneToOneField(User,
        unique=True,
        verbose_name=_('user'),
        related_name='my_profile',
        blank=True,
        null=True,
    )

    nickname = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

class Tournament(models.Model):
    '''
        Torneio evento de poker
        Relacionamento n pra n com player
        Relacionamento 1 pra n com itm

    '''
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    logo = models.ImageField(upload_to="tournament_logos",blank=True,null=True)

    buy_in = models.FloatField()
    qty_chips_buy_in = models.IntegerField()
    rebuy = models.FloatField()
    qty_chips_rebuy = models.IntegerField()
    add_on = models.FloatField()
    qty_chips_add_on = models.IntegerField()

    player = models.ManyToManyField(Player,related_name='player_tournaments')
    location = models.CharField(max_length=30)
    start_at = models.DateTimeField()
    total_avaliable_points = models.IntegerField(blank=True, null=True)
    total_money = models.FloatField(blank=True,null=True)
    total_buy_in = models.IntegerField()
    total_rebuy = models.IntegerField()
    total_add_on = models.IntegerField()

    def updateTotalMoney(self):
        #Calcula o total de dinheiro no prize pool
        self.total_money = (self.buy_in * self.total_buy_in)\
                           + (self.add_on * self.total_add_on)\
                           + (self.rebuy * self.total_rebuy)

        super(Tournament,self).save()

    def updateAvaliablePoints(self):
        self.total_avaliable_points = len(self.player.all())

        super(Tournament,self).save()

    def save(self, force_insert=False, force_update=False, using=None):
        #Salvo o objeto torneio
        super(Tournament,self).save()

        self.updateTotalMoney()
        self.updateAvaliablePoints()

    def __unicode__(self):
        return self.name

class Itm(models.Model):
    '''
        premiação de cada torneio
        relacionamento 1 para n com torneio
        e relacionamento 1 para n com jogador
    '''
    position = models.IntegerField()
    percent = models.FloatField()
    final_value = models.FloatField(blank=True)
    tournament = models.ForeignKey(Tournament)
    player = models.ForeignKey(Player)

    #Calcula o valor do itm
    def save(self, force_insert=False, force_update=False, using=None):
        self.final_value = self.tournament.total_money * (self.percent / 100)

        super(Itm,self).save()

    def __unicode__(self):
        return self.tournament.name + '-' + self.player.nickname

class News(models.Model):
    '''
        Noticias exibidas na home
    '''

    title = models.CharField(max_length=250)
    shortContent = models.CharField(max_length=160)
    content = models.TextField()
    photo = models.ImageField(upload_to='NewsPhoto')
    pub_date = models.DateTimeField(default=datetime.now , blank=True)
    user = models.ForeignKey(Player)
    like = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return self.title

class League(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=500)

    tournament = models.ForeignKey(Tournament)