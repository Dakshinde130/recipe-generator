# 🥘 FlavorFind — Recipe Generator

Tell it what's in your fridge, and it finds recipes you can make. A small
Spring Boot app that searches the [Spoonacular](https://spoonacular.com/food-api)
"find by ingredients" API and shows the results in a simple web UI.

## Requirements

- Java 17+
- Maven 3.9+
- A free Spoonacular API key — get one at <https://spoonacular.com/food-api/console#Dashboard>

## Configuration

The app reads your Spoonacular key from the `SPOONACULAR_API_KEY` environment
variable. **No key is stored in the source code** — you supply your own.

**Windows (PowerShell):**
```powershell
$env:SPOONACULAR_API_KEY = "your-key-here"
```

**Windows (cmd):**
```cmd
set SPOONACULAR_API_KEY=your-key-here
```

**macOS / Linux:**
```bash
export SPOONACULAR_API_KEY="your-key-here"
```

## Run

```bash
mvn spring-boot:run
```

Then open <http://localhost:8080> and enter some ingredients.

## Notes

- Keep your API key private. Do not paste it into the source or commit it.
- If a key is ever exposed, rotate it in the Spoonacular dashboard.
