package com.recipeapp.controller;
import com.recipeapp.model.Recipe;
import com.recipeapp.service.RecipeService;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/recipes")
@CrossOrigin(origins = "*")
public class RecipeController {
    private final RecipeService recipeService;
    public RecipeController(RecipeService recipeService) { this.recipeService = recipeService; }
    @GetMapping("/search")
    public List<Recipe> search(@RequestParam String ingredients) {
        return recipeService.getRecipesByIngredients(ingredients);
    }
}