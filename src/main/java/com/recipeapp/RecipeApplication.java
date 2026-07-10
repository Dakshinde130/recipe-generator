package com.recipeapp;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.core.env.Environment;

@SpringBootApplication
public class RecipeApplication {
    public static void main(String[] args) {
        SpringApplication.run(RecipeApplication.class, args);
    }

    // Prints a clickable link in the terminal once the app is up.
    // VS Code auto-detects the URL — Ctrl + click (Cmd + click on macOS) to open.
    @Bean
    CommandLineRunner printStartupUrl(Environment env) {
        return args -> {
            String port = env.getProperty("server.port", "8080");
            String url = "http://localhost:" + port;
            System.out.println();
            System.out.println("  ====================================================");
            System.out.println("   🥘  FlavorFind is live!");
            System.out.println("   👉  Open:  " + url);
            System.out.println("       (Ctrl + click the link above to launch it)");
            System.out.println("  ====================================================");
            System.out.println();
        };
    }
}