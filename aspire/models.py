from django.db import models

class Recipe(models.Model) :
    recipeId = models.IntegerField()
    title = models.CharField(max_length= 100)
    imgUrl = models.URLField(max_length= 1000)
    fat = models.IntegerField()
    protein = models.IntegerField()
    carbs = models.IntegerField()
    calories = models.IntegerField()

    def __str__(self) :
        return (self.title)

class User(models.Model) :
    email = models.EmailField(unique= True, max_length= 100)
    password = models.CharField(max_length= 20)
    firstName = models.CharField(max_length= 20)
    lastName = models.CharField(max_length= 20)

    def __str__(self) :
        name = self.firstName + ' ' + self.lastName
        return (name)

class Recipe_User(models.Model) :
    starred = models.BooleanField(default=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) :
        text = self.user.firstName + ' ' + self.user.lastName + '; ' + self.recipe.title 
        return (text)
        