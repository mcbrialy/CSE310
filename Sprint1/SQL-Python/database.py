"""SQLite data access for the recipe application."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


DATABASE_PATH = Path(__file__).with_name("recipes.db")


SAMPLE_RECIPES = [
    ("Classic Pancakes", 20, 4, "Whisk the dry ingredients. Add milk, egg, and melted butter. Cook ladlefuls on a hot griddle until golden on both sides.", [("2", "cups", "all-purpose flour"), ("2", "tbsp", "sugar"), ("1", "tbsp", "baking powder"), ("1 1/2", "cups", "milk"), ("1", "large", "egg")]),
    ("Vegetable Stir-Fry", 25, 3, "Stir-fry the vegetables in batches. Add the sauce and toss everything together until glossy. Serve over rice.", [("2", "cups", "broccoli"), ("1", "", "bell pepper"), ("1", "cup", "snow peas"), ("3", "tbsp", "soy sauce"), ("1", "tbsp", "sesame oil")]),
    ("Chicken Tikka Masala", 55, 4, "Marinate and sear the chicken. Simmer it in the spiced tomato cream sauce until tender. Garnish with cilantro.", [("1 1/2", "lb", "chicken thighs"), ("1", "cup", "tomato puree"), ("1/2", "cup", "heavy cream"), ("2", "tbsp", "garam masala"), ("1", "", "onion")]),
    ("Mushroom Risotto", 45, 4, "Sauté mushrooms and aromatics. Add rice and warm stock one ladle at a time, stirring until creamy. Finish with Parmesan.", [("1", "cup", "arborio rice"), ("8", "oz", "mushrooms"), ("4", "cups", "vegetable stock"), ("1/2", "cup", "Parmesan"), ("1/2", "cup", "white wine")]),
    ("Black Bean Tacos", 25, 4, "Warm the beans with cumin and lime. Fill tortillas with beans, cabbage, avocado, and salsa.", [("2", "cans", "black beans"), ("8", "", "corn tortillas"), ("1", "cup", "shredded cabbage"), ("1", "", "avocado"), ("1", "", "lime")]),
    ("Greek Salad", 15, 2, "Chop the vegetables and toss with feta, olives, oregano, and dressing.", [("2", "", "tomatoes"), ("1", "", "cucumber"), ("1/2", "", "red onion"), ("1/2", "cup", "feta cheese"), ("1/3", "cup", "Kalamata olives")]),
    ("Lentil Soup", 50, 6, "Sauté the vegetables, add lentils and broth, and simmer until tender. Season with lemon and herbs.", [("1 1/2", "cups", "green lentils"), ("6", "cups", "vegetable broth"), ("2", "", "carrots"), ("2", "stalks", "celery"), ("1", "", "lemon")]),
    ("Spaghetti Carbonara", 30, 4, "Cook pasta. Whisk eggs with cheese, then toss with hot pasta and crisp pancetta off the heat.", [("12", "oz", "spaghetti"), ("4", "oz", "pancetta"), ("2", "large", "eggs"), ("1", "cup", "Pecorino Romano"), ("1", "tsp", "black pepper")]),
    ("Baked Salmon", 30, 2, "Season the salmon and bake until just cooked. Serve with lemon and fresh herbs.", [("2", "fillets", "salmon"), ("1", "", "lemon"), ("2", "tbsp", "olive oil"), ("2", "tbsp", "dill"), ("1", "tsp", "garlic powder")]),
    ("Beef Chili", 75, 6, "Brown the beef, sauté the aromatics, then simmer with beans, tomatoes, and spices until thick.", [("1", "lb", "ground beef"), ("2", "cans", "kidney beans"), ("2", "cans", "diced tomatoes"), ("1", "", "onion"), ("2", "tbsp", "chili powder")]),
    ("Thai Peanut Noodles", 25, 3, "Cook noodles and vegetables. Whisk the peanut sauce, toss everything together, and top with peanuts.", [("8", "oz", "rice noodles"), ("1/3", "cup", "peanut butter"), ("2", "tbsp", "soy sauce"), ("1", "tbsp", "lime juice"), ("1", "cup", "shredded carrots")]),
    ("Shakshuka", 35, 3, "Simmer peppers and tomatoes with spices. Make wells, crack in eggs, cover, and cook until set.", [("1", "can", "crushed tomatoes"), ("1", "", "bell pepper"), ("4", "large", "eggs"), ("1", "tsp", "cumin"), ("1/2", "", "onion")]),
    ("Roasted Vegetable Quinoa Bowl", 40, 4, "Roast the vegetables. Serve over quinoa with chickpeas and lemon tahini dressing.", [("1", "cup", "quinoa"), ("2", "cups", "chickpeas"), ("2", "cups", "cauliflower"), ("1", "", "sweet potato"), ("1/4", "cup", "tahini")]),
    ("Turkey Meatballs", 45, 4, "Mix the ingredients, shape into meatballs, and bake. Serve with marinara and pasta or bread.", [("1", "lb", "ground turkey"), ("1/2", "cup", "breadcrumbs"), ("1", "large", "egg"), ("1/4", "cup", "Parmesan"), ("2", "cups", "marinara sauce")]),
    ("Apple Cinnamon Oatmeal", 12, 2, "Simmer oats with milk. Stir in diced apple, cinnamon, and maple syrup.", [("1", "cup", "rolled oats"), ("2", "cups", "milk"), ("1", "", "apple"), ("1", "tsp", "cinnamon"), ("1", "tbsp", "maple syrup")]),
    ("Tuna Pasta Salad", 25, 4, "Cook and cool the pasta. Mix with tuna, vegetables, and creamy dressing. Chill before serving.", [("8", "oz", "rotini"), ("2", "cans", "tuna"), ("1/2", "cup", "mayonnaise"), ("1/2", "cup", "peas"), ("1", "stalk", "celery")]),
    ("Coconut Curry Chickpeas", 35, 4, "Sauté aromatics and spices, add chickpeas and coconut milk, and simmer. Serve with rice.", [("2", "cans", "chickpeas"), ("1", "can", "coconut milk"), ("2", "tbsp", "curry paste"), ("1", "", "onion"), ("2", "cups", "spinach")]),
    ("French Toast", 20, 4, "Dip bread in the egg mixture and cook in butter until golden. Serve with berries and syrup.", [("8", "slices", "brioche"), ("3", "large", "eggs"), ("1/2", "cup", "milk"), ("1", "tsp", "vanilla"), ("1", "tsp", "cinnamon")]),
    ("Miso Ramen", 30, 2, "Prepare the broth with miso and aromatics. Add noodles and vegetables, then top with egg and scallions.", [("2", "packs", "ramen noodles"), ("4", "cups", "vegetable broth"), ("3", "tbsp", "white miso"), ("2", "", "eggs"), ("1", "cup", "bok choy")]),
    ("Sheet-Pan Sausage and Peppers", 40, 4, "Toss sausage and vegetables with oil and herbs. Roast on one pan until browned and tender.", [("1", "lb", "Italian sausage"), ("2", "", "bell peppers"), ("1", "", "red onion"), ("1", "lb", "baby potatoes"), ("2", "tbsp", "olive oil")]),
    ("Guacamole", 15, 4, "Mash avocados with lime, onion, tomato, cilantro, and salt. Serve immediately.", [("3", "", "avocados"), ("1", "", "lime"), ("1/4", "", "red onion"), ("1", "", "tomato"), ("2", "tbsp", "cilantro")]),
    ("Blueberry Muffins", 35, 12, "Mix the batter gently, fold in blueberries, and bake until golden and a tester comes out clean.", [("2", "cups", "all-purpose flour"), ("1", "cup", "blueberries"), ("1/2", "cup", "sugar"), ("1", "large", "egg"), ("1/2", "cup", "milk")]),
    ("Pulled Pork Sliders", 240, 8, "Season and slow-cook the pork until tender. Shred it and serve on slider buns with barbecue sauce.", [("3", "lb", "pork shoulder"), ("1", "cup", "barbecue sauce"), ("8", "", "slider buns"), ("2", "cups", "coleslaw"), ("2", "tbsp", "brown sugar")]),
    ("Falafel Pitas", 50, 4, "Blend soaked chickpeas with herbs and spices. Shape and bake or fry, then serve in pita with tahini.", [("2", "cups", "dried chickpeas"), ("1/2", "cup", "parsley"), ("2", "cloves", "garlic"), ("4", "", "pitas"), ("1/3", "cup", "tahini")]),
    ("Creamy Tomato Soup", 40, 4, "Sauté aromatics, simmer tomatoes with broth, blend smooth, and finish with cream.", [("2", "cans", "whole tomatoes"), ("4", "cups", "vegetable broth"), ("1", "", "onion"), ("1/2", "cup", "heavy cream"), ("1", "tsp", "dried basil")]),
    ("Teriyaki Tofu Bowls", 35, 3, "Press and crisp the tofu. Cook with teriyaki sauce and serve over rice with steamed broccoli.", [("14", "oz", "firm tofu"), ("1/3", "cup", "teriyaki sauce"), ("2", "cups", "broccoli"), ("2", "cups", "cooked rice"), ("1", "tbsp", "sesame seeds")]),
    ("Chocolate Mug Cake", 8, 1, "Whisk ingredients in a mug and microwave until just set. Rest briefly before serving.", [("4", "tbsp", "flour"), ("2", "tbsp", "cocoa powder"), ("2", "tbsp", "sugar"), ("3", "tbsp", "milk"), ("1", "tbsp", "chocolate chips")]),
    ("Mediterranean Couscous", 20, 4, "Pour hot broth over couscous and let it steam. Fluff with a fork and fold in vegetables, herbs, and feta.", [("1 1/2", "cups", "couscous"), ("1 1/2", "cups", "vegetable broth"), ("1", "cup", "cherry tomatoes"), ("1/2", "cup", "feta"), ("1/4", "cup", "parsley")]),
    ("Vegetable Frittata", 30, 6, "Sauté vegetables, pour over beaten eggs, and cook until nearly set. Finish under the broiler.", [("8", "large", "eggs"), ("1", "cup", "spinach"), ("1/2", "", "bell pepper"), ("1/2", "cup", "cheddar cheese"), ("1", "", "onion")]),
    ("Beef and Broccoli", 30, 4, "Sear thin beef strips, stir-fry broccoli, and toss with the savory sauce. Serve over rice.", [("1", "lb", "flank steak"), ("4", "cups", "broccoli"), ("1/4", "cup", "soy sauce"), ("1", "tbsp", "cornstarch"), ("2", "cups", "cooked rice")]),
]


class RecipeDatabase:
    """Encapsulates all SQLite operations used by the GUI."""

    def __init__(self, database_path: Path | str = DATABASE_PATH) -> None:
        self.database_path = str(database_path)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS recipes (
                    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                    prep_time INTEGER NOT NULL CHECK (prep_time > 0),
                    servings INTEGER NOT NULL CHECK (servings > 0),
                    instructions TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS ingredients (
                    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL COLLATE NOCASE UNIQUE
                );

                CREATE TABLE IF NOT EXISTS recipe_ingredients (
                    recipe_id INTEGER NOT NULL,
                    ingredient_id INTEGER NOT NULL,
                    quantity TEXT NOT NULL,
                    unit TEXT NOT NULL,
                    PRIMARY KEY (recipe_id, ingredient_id),
                    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
                        ON DELETE CASCADE,
                    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id)
                        ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS app_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                """
            )
            seeded = connection.execute(
                "SELECT value FROM app_metadata WHERE key = 'sample_data_seeded'"
            ).fetchone()
            if seeded is None:
                self._insert_sample_recipes(connection)
                connection.execute(
                    "INSERT INTO app_metadata (key, value) VALUES ('sample_data_seeded', '1')"
                )

    @staticmethod
    def _insert_sample_recipes(connection: sqlite3.Connection) -> None:
        for name, prep_time, servings, instructions, ingredients in SAMPLE_RECIPES:
            cursor = connection.execute(
                """
                INSERT INTO recipes (name, prep_time, servings, instructions)
                VALUES (?, ?, ?, ?)
                """,
                (name, prep_time, servings, instructions),
            )
            recipe_id = cursor.lastrowid
            for quantity, unit, ingredient_name in ingredients:
                connection.execute(
                    "INSERT OR IGNORE INTO ingredients (name) VALUES (?)",
                    (ingredient_name,),
                )
                ingredient_id = connection.execute(
                    "SELECT ingredient_id FROM ingredients WHERE name = ?",
                    (ingredient_name,),
                ).fetchone()["ingredient_id"]
                connection.execute(
                    """
                    INSERT INTO recipe_ingredients
                        (recipe_id, ingredient_id, quantity, unit)
                    VALUES (?, ?, ?, ?)
                    """,
                    (recipe_id, ingredient_id, quantity, unit),
                )

    def list_recipes(self, search: str = "") -> list[sqlite3.Row]:
        search = search.strip()
        with self.connect() as connection:
            if search:
                pattern = f"%{search}%"
                return connection.execute(
                    """
                    SELECT DISTINCT r.recipe_id, r.name, r.prep_time, r.servings
                    FROM recipes AS r
                    LEFT JOIN recipe_ingredients AS ri ON ri.recipe_id = r.recipe_id
                    LEFT JOIN ingredients AS i ON i.ingredient_id = ri.ingredient_id
                    WHERE r.name LIKE ? OR i.name LIKE ?
                    ORDER BY r.name COLLATE NOCASE
                    """,
                    (pattern, pattern),
                ).fetchall()

            return connection.execute(
                """
                SELECT recipe_id, name, prep_time, servings
                FROM recipes
                ORDER BY name COLLATE NOCASE
                """
            ).fetchall()

    def get_recipe(self, recipe_id: int) -> dict[str, Any] | None:
        with self.connect() as connection:
            recipe = connection.execute(
                "SELECT * FROM recipes WHERE recipe_id = ?", (recipe_id,)
            ).fetchone()
            if recipe is None:
                return None

            ingredients = connection.execute(
                """
                SELECT i.name, ri.quantity, ri.unit
                FROM recipe_ingredients AS ri
                JOIN ingredients AS i ON i.ingredient_id = ri.ingredient_id
                WHERE ri.recipe_id = ?
                ORDER BY ri.rowid
                """,
                (recipe_id,),
            ).fetchall()

        return {
            "recipe_id": recipe["recipe_id"],
            "name": recipe["name"],
            "prep_time": recipe["prep_time"],
            "servings": recipe["servings"],
            "instructions": recipe["instructions"],
            "ingredients": [dict(ingredient) for ingredient in ingredients],
        }

    def save_recipe(
        self,
        name: str,
        prep_time: int,
        servings: int,
        instructions: str,
        ingredients: list[dict[str, str]],
        recipe_id: int | None = None,
    ) -> int:
        with self.connect() as connection:
            if recipe_id is None:
                cursor = connection.execute(
                    """
                    INSERT INTO recipes (name, prep_time, servings, instructions)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, prep_time, servings, instructions),
                )
                recipe_id = int(cursor.lastrowid)
            else:
                connection.execute(
                    """
                    UPDATE recipes
                    SET name = ?, prep_time = ?, servings = ?, instructions = ?
                    WHERE recipe_id = ?
                    """,
                    (name, prep_time, servings, instructions, recipe_id),
                )
                connection.execute(
                    "DELETE FROM recipe_ingredients WHERE recipe_id = ?", (recipe_id,)
                )

            for ingredient in ingredients:
                connection.execute(
                    "INSERT OR IGNORE INTO ingredients (name) VALUES (?)",
                    (ingredient["name"],),
                )
                ingredient_row = connection.execute(
                    "SELECT ingredient_id FROM ingredients WHERE name = ?",
                    (ingredient["name"],),
                ).fetchone()
                connection.execute(
                    """
                    INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, unit)
                    VALUES (?, ?, ?, ?)
                    """,
                    (recipe_id, ingredient_row["ingredient_id"], ingredient["quantity"], ingredient["unit"]),
                )

        return recipe_id

    def delete_recipe(self, recipe_id: int) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM recipes WHERE recipe_id = ?", (recipe_id,))
