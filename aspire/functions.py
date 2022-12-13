import math
toph_api_key = 'ffcbb1d69amsh90230347f7931d3p1536aejsn25568159361e'
mckenna_api_key = '33ea8e8ec5msh5b89e2129e49ef7p1ad746jsnc923290b266f'
corban_api_key = '4280b68f46mshaf658c384f5e5a5p1b442bjsn0a6f338351ad'
api_key = mckenna_api_key

def searchRecipesFiltered(includeIngredientsList = [], excludeIngredientsList = [], minCarbs = 0, maxCarbs = 100, minProtein = 0, maxProtein = 100, minCalories = 0, maxCalories = 1200, minFat = 0, maxFat = 100):


    import requests
    includeString = ''
    for j in includeIngredientsList:
        length = len(includeIngredientsList)
        if includeIngredientsList.index(j) == length - 1:
            includeString += j
        else:
            includeString += j
            includeString += ','

    excludeString = ''
    for h in excludeIngredientsList:
        length = len(excludeIngredientsList)
        if excludeIngredientsList.index(h) == length - 1:
            excludeString += h
        else:
            excludeString += h
            excludeString += ','

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

    querystring = {"query":"", #this is the only required parameter. It is what will be entered in the 'search bar'.
                    "includeIngredients":includeString,
                "excludeIngredients":excludeString,
                    "minCarbs":minCarbs,
                "maxCarbs":maxCarbs,
                "minProtein":minProtein,
                "maxProtein":maxProtein,
                "minCalories":minCalories,
                "maxCalories":maxCalories,
                "minFat":minFat,
                "maxFat":maxFat                    
    }



    headers = {
        "X-RapidAPI-Key": "04fb037d86mshbc10cd2bcf9efc3p1b1aa2jsnb5518a2797b1",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r = response.json()
    
    
    recipeList = []

    for i in r['results']:
        thisList = []
        thisList.append(i['title'])
        thisList.append(i['id'])
        thisList.append(i['image'])
        recipeList.append(thisList)

    
    return(recipeList)


#@title Get Recipe Information
def getRecipeInfo(id):
    import requests
    recipeID = id #change this once we get another input
    recipeID = str(recipeID)

    url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipeID}/information"


    querystring = {"stepBreakdown":"true", "includeNutrition":"true"}

    headers = {
        "X-RapidAPI-Key": "04fb037d86mshbc10cd2bcf9efc3p1b1aa2jsnb5518a2797b1",
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    r = response.json()

    ingredientDict = {}
    for i  in r['extendedIngredients']:
        amountString = str(i['amount']) + ' ' + str(i['unit'])
        ingredientDict[i['name']] = amountString

    instructionsDict = {}
    for i in r['analyzedInstructions'][0]['steps']:
        instructionsDict[i['number']] = i['step']

    nutrientDict = {}
    for i in r['nutrition']['nutrients']:
        if i['name'] == 'Calories':
            amountString = i['amount']
            nutrientDict[i['name']] = amountString
        elif i['name'] == 'Protein':
            amountString = i['amount'] 
            nutrientDict[i['name']] = amountString
        elif i['name'] == 'Fat':
            amountString = i['amount']
            nutrientDict[i['name']] = amountString
        elif i['name'] == 'Carbohydrates':
            amountString = i['amount']
            nutrientDict[i['name']] = amountString  
        else:
            pass
    title = r['title']
    imgUrl = r['image']

    
    return title, imgUrl, ingredientDict, instructionsDict, nutrientDict

def round(val):
    return int(math.ceil(val))

