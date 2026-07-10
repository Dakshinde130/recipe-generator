package com.recipeapp.service;
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
        if (API_KEY == null || API_KEY.isBlank()) {
            System.err.println("SPOONACULAR_API_KEY environment variable is not set — returning no results.");
            return new ArrayList<>();
        }
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
}