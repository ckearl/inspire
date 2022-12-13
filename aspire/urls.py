from django.urls import path
from .views import indexPageView, loginPageView, savedPageView, recipePageView, savedUserPageView, \
    savedLoginPageView, addRecipePageView, registerPageView, deleteRecipePageView, starRecipePageView

urlpatterns = [
    path("", indexPageView, name="index"),
    path("login/", loginPageView, name="login"),   
    path("register/", registerPageView, name="register"),   
    path("register/<int:try_again>", registerPageView, name="register"),   
    path("saved/<int:user_id>", savedPageView, name="saved"), 
    path("recipe/<int:user_id>/<int:recipe_id>", recipePageView, name="recipe"), 
    path("saved_user/", savedUserPageView, name="saved_user"), 
    path("saved_login/", savedLoginPageView, name="saved_login"), 
    path("add_recipe/<int:user_id>/<int:recipe_id>", addRecipePageView, name="add_recipe"), 
    path("delete_recipe/<int:user_id>/<int:recipe_id>", deleteRecipePageView, name="delete_recipe"), 
    path("star_recipe/<int:user_id>/<int:recipe_id>", starRecipePageView, name="star_recipe"), 


]     