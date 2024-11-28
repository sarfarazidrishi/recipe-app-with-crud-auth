from django.shortcuts import render, redirect
from . models import Recipe
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def recipes(request):
    if request.method == "POST":
        data = request.POST
        recipe_title = data.get('recipe_title')
        recipe_description = data.get('recipe_description')
        recipeImg=request.FILES.get('recipeImg')
 
        Recipe.objects.create(
            recipe_title = recipe_title,
            recipe_description = recipe_description,
            recipeImg = recipeImg,
        )
        
        return redirect(reverse('vege:recipes'))
    
    queryset = Recipe.objects.all()
    if request.GET.get("search"):
        search_term=request.GET.get("search") #the search in this line is name of search filed that is being used to parse search term to this view 
        queryset = queryset.filter(Q(recipe_title__icontains = search_term) | Q(recipe_description__icontains=search_term))
    context = {'recipes': queryset}
    return render(request, 'recipes.html', context)

def delete_recipe(request, id):
    itemdel =  Recipe.objects.get(id = id)
    itemdel.delete()
    return redirect('/')

def update_recipe(request, id):
    itemupdate= Recipe.objects.get(id=id)
    if request.method == "POST":
        data = request.POST
        recipe_title= data.get('recipe_title')
        recipe_description= data.get('recipe_description')
        recipeImg= request.FILES.get('recipeImg')

        itemupdate.recipe_title = recipe_title
        itemupdate.recipe_description = recipe_description
        if recipeImg:
            itemupdate.recipeImg = recipeImg
        
        itemupdate.save()

        return redirect('/')                                               

    context= {'recipe': itemupdate}
    return render(request, 'updaterecipe.html', context)

def allrecipes(request):
      allrecipes = Recipe.objects.all()
      if request.GET.get("search"):
        search_term=request.GET.get("search")
        allrecipes = allrecipes.filter(Q(recipe_title__icontains = search_term) | Q(recipe_description__icontains=search_term))
        context = {'allrecipes': allrecipes}
      return render(request, 'allrecipes.html', {'allrecipes':allrecipes})