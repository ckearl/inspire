from django.http import HttpResponse
from django.shortcuts import render
from .functions import searchRecipesFiltered, getRecipeInfo
from .models import User, Recipe, Recipe_User
from datetime import datetime
from django.http import HttpResponse

def indexPageView(request) :
    return render(request, 'aspire/index.html')

def loginPageView(request) :
    return render(request, 'aspire/login.html')

def registerPageView(request, try_again=1) :
    context = {
        'try_again' : try_again
    }
    return render(request, 'aspire/register.html', context)

def savedUserPageView(request) :
    #this generates a new user object using the information received through registering
    new_user = User()
    new_user.firstName = request.POST.get('first_name')
    new_user.lastName = request.POST.get('last_name')
    new_user.email = request.POST.get('inputEmail')
    new_user.password = request.POST.get('inputPassword')
    try :
        new_user.save()
    except :
        return registerPageView(request, try_again=2)

    return savedPageView(request, new_user.id)

def savedLoginPageView (request) :
    useremail = request.POST.get('email')
    userpassword = request.POST.get('password')

    #checks if the useremail and password match
    try :
        user = User.objects.get(email = useremail, password = userpassword)

    except :

        return render(request, 'aspire/login.html')

    return savedPageView(request, user.id)

def savedPageView(request, user_id) :
    user = User.objects.get(id = user_id)

    # gets ingredients to include
    includeIngredientsString = request.GET.get('choices-text-preset-values')
    includeIngredientsList = list()
    if includeIngredientsString != None :
        includeIngredientsList = includeIngredientsString.split(',')
        for ingredient in range(0, len(includeIngredientsList)) :
            includeIngredientsList[ingredient] = includeIngredientsList[ingredient].strip()

    # gets min max values for each macro
    max_min_carbs = request.GET.get('max-min-carbs')
    max_min_protein = request.GET.get('max-min-protein')
    max_min_fat = request.GET.get('max-min-fat')
    max_min_calories = request.GET.get('max-min-calories')
    if max_min_carbs == 'min' :
        minCarbs = request.GET.get('carbs-val')
        maxCarbs = None
    else :
        maxCarbs = request.GET.get('carbs-val')
        minCarbs = None
    if max_min_protein == 'min' :
        minProtein = request.GET.get('protein-val')
        maxProtein = None
    else :
        maxProtein = request.GET.get('protein-val')
        minProtein = None
    if max_min_fat == 'min' :
        minFat = request.GET.get('fat-val')
        maxFat = None
    else :
        maxFat = request.GET.get('fat-val')
        minFat = None
    if max_min_calories == 'min' :
        minCalories = request.GET.get('calories-val')
        maxCalories = None
    else :
        maxCalories = request.GET.get('calories-val')
        minCalories = None

    # gets ingredients to avoid
    excludeIngredientsString = request.GET.get('choices-text-preset-values-exclude')
    excludeIngredientsList = list()
    if excludeIngredientsString != None:
        excludeIngredientsList = excludeIngredientsString.split(',')
    gluten_check = request.GET.get('gluten-check')
    dairy_check = request.GET.get('dairy-check')
    soy_check = request.GET.get('soy-check')
    nuts_check = request.GET.get('nuts-check')
    sugar_check = request.GET.get('sugar-check')
    if gluten_check != None : excludeIngredientsList.append(gluten_check)
    if dairy_check != None : excludeIngredientsList.append(dairy_check)
    if soy_check != None : excludeIngredientsList.append(soy_check)
    if nuts_check != None : excludeIngredientsList.append(nuts_check)
    if sugar_check != None : excludeIngredientsList.append(sugar_check)

    # gets list of recipes that match search criteria
    if bool(includeIngredientsList) == True :
        search_recipe_list = searchRecipesFiltered(includeIngredientsList, excludeIngredientsList, minCarbs, maxCarbs, minProtein, maxProtein, minCalories, maxCalories, minFat, maxFat)
    else :
        search_recipe_list = list()

    # gets list of recipes the user has saved
    recipe_user_list = Recipe_User.objects.filter(user = user_id)
    recipe_obj_list = list()
    for recipe_user in recipe_user_list :
        recipe_obj_list.append((Recipe.objects.get(recipeId = recipe_user.recipe.recipeId)))

    context = {
            'user' : user,
            'recipe_user_list' : recipe_user_list,
            'recipe_obj_list' : recipe_obj_list,
            'search_recipe_list' : search_recipe_list,
        }

    return render(request, 'aspire/saved.html', context)

#this allows a user to add recipes to their record
def addRecipePageView(request, user_id, recipe_id) :
    user = User.objects.get(id = user_id)

    title, imgUrl, ingredient_dict, instructions_dict, nutrient_dict = getRecipeInfo(recipe_id)
    


    new_recipe = Recipe()

    new_recipe.title = title
    new_recipe.recipeId = recipe_id
    new_recipe.imgUrl = imgUrl
    new_recipe.fat = nutrient_dict['Fat']
    new_recipe.protein = nutrient_dict['Protein']
    new_recipe.carbs = nutrient_dict['Carbohydrates']
    new_recipe.calories = nutrient_dict['Calories'] 
    new_recipe.save()

    new_recipe_user = Recipe_User()
    new_recipe_user.recipe = new_recipe
    new_recipe_user.user = user
    new_recipe_user.save()

    return savedPageView(request, user_id)

def deleteRecipePageView(request, user_id, recipe_id) :
    user = User.objects.get(id = user_id)
    recipe = Recipe.objects.get(recipeId = recipe_id)

    recipe_user = Recipe_User.objects.get(recipe = recipe, user = user)


    recipe_user.delete()

    return savedPageView(request, user_id)

def starRecipePageView(request, user_id, recipe_id) :
    user = User.objects.get(id = user_id)
    recipe = Recipe.objects.get(recipeId = recipe_id)

    recipe_user = Recipe_User.objects.get(recipe = recipe, user = user)

    
    recipe_user_starred = request.POST.get('star-recipe')
    if recipe_user_starred == 'starred' :
        recipe_user.starred = True
    else :
        recipe_user.starred = False
    recipe_user.save()


    return savedPageView(request, user_id)

def recipePageView(request, user_id, recipe_id) :
    user = User.objects.get(id = user_id)
    title, imgUrl, ingredient_dict, instructions_dict, nutrient_dict = getRecipeInfo(recipe_id)
    recipe = ''
    recipe_user = ''
    try :
        recipe = Recipe.objects.get(recipeId = recipe_id)
        recipe_user = Recipe_User.objects.get(recipe = recipe, user = user)
        saved = True
    except :
        saved = False



    context = {
        'user' : user,
        'recipe' : recipe,
        'recipe_user' : recipe_user,
        'title' : title,
        'imgUrl' : imgUrl,
        'ingredient_dict' : ingredient_dict,
        'instructions_dict' : instructions_dict,
        'nutrient_dict' : nutrient_dict,
        'saved' : saved,
        'recipe_id' : recipe_id,
    }
    return render(request, 'aspire/recipe.html', context)

