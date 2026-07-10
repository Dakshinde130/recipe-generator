package com.recipeapp.service;
import com.recipeapp.model.Recipe;
import java.util.List;
public interface RecipeService {
    List<Recipe> getRecipesByIngredients(String ingredients);
}