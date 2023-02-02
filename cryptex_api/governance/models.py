from django.db import models


class CryptKeeper(models.Model):
    address = models.CharField(u'Address', max_length=128, unique=True )
    name = models.CharField(u'Name', max_length=75)
    eth_name = models.CharField(u'Eth Name', max_length=128)
    expertise = models.CharField(u'Expertise', max_length=120)
    why = models.CharField(u'Why', max_length=4000)
    image = models.CharField(u'Image', max_length=255)
    discord = models.CharField(u'Discord', max_length=30)
    twitter = models.CharField(u'Twitter', max_length=30)

    class Meta:
        verbose_name = u'Crypt. Keeper'
        verbose_name_plural = u'Crypt. Keepers'
