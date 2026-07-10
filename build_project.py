import os

# Define the folder structure and file contents
project_structure = {
    "pom.xml": """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>
    <groupId>com.recipeapp</groupId>
    <artifactId>recipe-generator</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.10.1</version>
        </dependency>
    </dependencies>
    <properties>
        <java.version>17</java.version>
    </properties>
</project>""",

    "src/main/java/com/recipeapp/RecipeApplication.java": """package com.recipeapp;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class RecipeApplication {
    public static void main(String[] args) {
        SpringApplication.run(RecipeApplication.class, args);
    }
}""",

    "src/main/java/com/recipeapp/model/Recipe.java": """package com.recipeapp.model;
public record Recipe(String title, String image, int id) {}""",

    "src/main/java/com/recipeapp/service/RecipeService.java": """package com.recipeapp.service;
import com.recipeapp.model.Recipe;
import java.util.List;
public interface RecipeService {
    List<Recipe> getRecipesByIngredients(String ingredients);
}""",

    "src/main/java/com/recipeapp/service/SpoonacularService.java": """package com.recipeapp.service;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.recipeapp.model.Recipe;
import org.springframework.stereotype.Service;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

@Service
public class SpoonacularService implements RecipeService {
    // Read the key from the SPOONACULAR_API_KEY environment variable — never hardcode secrets.
    private final String API_KEY = System.getenv("SPOONACULAR_API_KEY");
    private final String BASE_URL = "https://api.spoonacular.com/recipes/findByIngredients";
    private final HttpClient client = HttpClient.newHttpClient();
    private final Gson gson = new Gson();

    @Override
    public List<Recipe> getRecipesByIngredients(String ingredients) {
        String url = String.format("%s?ingredients=%s&number=6&apiKey=%s", BASE_URL, ingredients, API_KEY);
        HttpRequest request = HttpRequest.newBuilder().uri(URI.create(url)).GET().build();
        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            JsonArray array = gson.fromJson(response.body(), JsonArray.class);
            List<Recipe> recipes = new ArrayList<>();
            for (JsonElement e : array) {
                JsonObject obj = e.getAsJsonObject();
                recipes.add(new Recipe(obj.get("title").getAsString(), obj.get("image").getAsString(), obj.get("id").getAsInt()));
            }
            return recipes;
        } catch (Exception e) { return new ArrayList<>(); }
    }
}""",

    "src/main/java/com/recipeapp/controller/RecipeController.java": """package com.recipeapp.controller;
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
}""",

    "src/main/resources/static/index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FlavorFind | Ingredients In, Dinner Out</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); }
        .glass { background: rgba(255, 255, 255, 0.25); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.18); }
        .recipe-card:hover { transform: translateY(-10px); transition: all 0.3s ease; }
    </style>
</head>
<body class="min-h-screen p-4 md:p-10">
    <div class="max-w-6xl mx-auto">
        <header class="text-center mb-12">
            <h1 class="text-5xl font-bold text-white drop-shadow-lg mb-2">🥘 FlavorFind</h1>
            <p class="text-white text-lg opacity-90">"Tell it what's in your fridge. It figures out the rest."</p>
        </header>
        <div class="glass p-8 rounded-3xl shadow-2xl max-w-2xl mx-auto mb-12 text-center">
            <div class="flex flex-col md:flex-row gap-4">
                <input type="text" id="ingredientInput" placeholder="Enter ingredients (e.g. tomato, pasta, garlic)" 
                    class="w-full px-6 py-4 rounded-full outline-none focus:ring-4 ring-orange-300 text-gray-700 text-lg">
                <button onclick="searchRecipes()" 
                    class="bg-orange-600 hover:bg-orange-700 text-white font-bold px-8 py-4 rounded-full transition-all duration-300 shadow-lg">
                    Find Dinner
                </button>
            </div>
        </div>
        <div id="recipeGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"></div>
    </div>
    <script>
        async function searchRecipes() {
            const ingredients = document.getElementById('ingredientInput').value;
            const grid = document.getElementById('recipeGrid');
            if (!ingredients) return alert("Please enter some ingredients!");
            grid.innerHTML = `<div class="col-span-full text-center text-white text-2xl">Searching for delicious ideas...</div>`;
            try {
                const response = await fetch(`/api/recipes/search?ingredients=${ingredients}`);
                const recipes = await response.json();
                grid.innerHTML = ''; 
                if (recipes.length === 0) {
                    grid.innerHTML = `<div class="col-span-full text-center text-white text-xl">No recipes found. Try adding more items!</div>`;
                    return;
                }
                recipes.forEach(recipe => {
                    grid.innerHTML += `
                        <div class="recipe-card glass rounded-3xl overflow-hidden shadow-xl text-gray-800">
                            <img src="${recipe.image}" class="w-full h-48 object-cover" alt="${recipe.title}">
                            <div class="p-6">
                                <h3 class="text-xl font-bold mb-4 truncate">${recipe.title}</h3>
                                <button onclick="window.open('https://www.google.com/search?q=${recipe.title}+recipe')" 
                                    class="w-full py-2 bg-white text-orange-600 font-semibold rounded-xl hover:bg-orange-100 transition-colors">
                                    View Recipe →
                                </button>
                            </div>
                        </div>`;
                });
            } catch (error) { grid.innerHTML = `<div class="col-span-full text-center text-white">Error connecting to server.</div>`; }
        }
    </script>
</body>
</html>"""
}

# Script to create the folders and files
for path, content in project_structure.items():
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("\n✅ PROJECT GENERATED SUCCESSFULLY!")
print("1. Open the 'recipe-generator' folder in VS Code.")
print("2. Set the SPOONACULAR_API_KEY environment variable to your key.")
print("3. Run RecipeApplication.java")
