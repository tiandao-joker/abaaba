from django.contrib import admin
from .models import MoviesType, Movies, MoviesSKU, IndexMoviesBanner, IndexTypeMoviesBanner,VipMovies,UserMoviesComment

# Register your models here.

admin.site.register(Movies)
admin.site.register(MoviesType)
admin.site.register(MoviesSKU)
admin.site.register(IndexMoviesBanner)
admin.site.register(IndexTypeMoviesBanner)
admin.site.register(UserMoviesComment)
admin.site.register(VipMovies)