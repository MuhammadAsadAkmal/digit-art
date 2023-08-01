from django_hosts import patterns, host
from django.contrib import admin

host_patterns = patterns(
    '',
    host(r'artista', 'artGalleryMain.urls', name='www'),
    host(r'artist', 'adminArtist.urls', name='artist'),
    host(r'artistaapi', 'artGalleryApp.urls', name='app'),
)
