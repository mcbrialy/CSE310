"""Professional Tkinter GUI for managing recipes in SQLite."""


from __future__ import annotations

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from database import RecipeDatabase


class RecipeApp(tk.Tk):
    CREAM = "#F3F7F8"
    CREAM_DARK = "#DCE8EA"
    NAVY = "#17324D"
    TERRACOTTA = "#E06B5A"
    TERRACOTTA_DARK = "#B94F43"
    SAGE = "#168C8C"
    SAGE_DARK = "#106B70"
    INK = "#20343F"
    MUTED = "#62747D"
    WHITE = "#FFFFFF"

    def __init__(self) -> None:
        super().__init__()
        self.database = RecipeDatabase()
        self.selected_recipe_id: int | None = None
        self.ingredient_rows: list[tuple[ttk.Entry, ttk.Entry, ttk.Entry]] = []

        self.title("Recipe Manager")
        self.geometry("1050x680")
        self.minsize(900, 600)
        self.configure(bg=self.CREAM)
        self._configure_style()
        self._build_layout()
        self.refresh_recipe_list()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("App.TFrame", background=self.CREAM)
        style.configure("Header.TLabel", background=self.NAVY, foreground=self.WHITE, font=("Segoe UI", 22, "bold"), padding=(24, 20))
        style.configure("Section.TLabel", background=self.CREAM, foreground=self.INK, font=("Segoe UI", 13, "bold"))
        style.configure("Muted.TLabel", background=self.CREAM, foreground=self.MUTED, font=("Segoe UI", 10))
        style.configure("TLabel", background=self.CREAM, foreground=self.INK, font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground=self.WHITE, foreground=self.INK, bordercolor=self.CREAM_DARK, lightcolor=self.CREAM_DARK, darkcolor=self.CREAM_DARK, padding=8)
        style.map("TEntry", bordercolor=[("focus", self.SAGE)])
        style.configure("Primary.TButton", background=self.TERRACOTTA, foreground=self.WHITE, padding=(14, 9), font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("Primary.TButton", background=[("active", self.TERRACOTTA_DARK)])
        style.configure("TButton", background=self.CREAM_DARK, foreground=self.INK, padding=(12, 8), font=("Segoe UI", 10), borderwidth=0)
        style.map("TButton", background=[("active", "#E4D4BD")])
        style.configure("Danger.TButton", background=self.SAGE, foreground=self.WHITE, padding=(12, 8), font=("Segoe UI", 10), borderwidth=0)
        style.map("Danger.TButton", background=[("active", self.SAGE_DARK)])
        style.configure("Treeview", background=self.WHITE, fieldbackground=self.WHITE, foreground=self.INK, rowheight=34, borderwidth=0, font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", self.SAGE)], foreground=[("selected", self.WHITE)])
        style.configure("Treeview.Heading", background=self.CREAM_DARK, foreground=self.INK, font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Treeview.Heading", background=[("active", "#E4D4BD")])
        style.configure("Vertical.TScrollbar", background=self.CREAM_DARK, troughcolor=self.CREAM, arrowcolor=self.INK, borderwidth=0)

    def _build_layout(self) -> None:
        header = ttk.Label(self, text="Recipe Manager", style="Header.TLabel")
        header.pack(fill="x")

        content = ttk.Frame(self, style="App.TFrame", padding=18)
        content.pack(fill="both", expand=True)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(1, weight=1)

        ttk.Label(content, text="Explore your recipes", style="Section.TLabel").grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Label(content, text="Recipe details", style="Section.TLabel").grid(row=0, column=1, sticky="w", padx=(18, 0), pady=(0, 8))

        list_frame = ttk.Frame(content, style="App.TFrame")
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.rowconfigure(1, weight=1)
        list_frame.columnconfigure(0, weight=1)

        search_frame = ttk.Frame(list_frame, style="App.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        search_frame.columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        search_entry.bind("<Return>", lambda _event: self.refresh_recipe_list())
        ttk.Button(search_frame, text="Search", command=self.refresh_recipe_list).grid(row=0, column=1, padx=2)
        ttk.Button(search_frame, text="Clear", command=self.clear_search).grid(row=0, column=2, padx=2)

        cards_frame = ttk.Frame(list_frame, style="App.TFrame")
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.rowconfigure(0, weight=1)
        cards_frame.columnconfigure(0, weight=1)
        self.cards_canvas = tk.Canvas(cards_frame, background=self.CREAM, highlightthickness=0, borderwidth=0)
        self.cards_canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(cards_frame, orient="vertical", command=self.cards_canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.cards_canvas.configure(yscrollcommand=scrollbar.set)
        self.cards_container = tk.Frame(self.cards_canvas, background=self.CREAM)
        self.cards_window = self.cards_canvas.create_window((0, 0), window=self.cards_container, anchor="nw")
        self.cards_container.bind("<Configure>", lambda _event: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all")))
        self.cards_canvas.bind("<Configure>", lambda event: self.cards_canvas.itemconfigure(self.cards_window, width=event.width))
        self.card_widgets: dict[int, tk.Frame] = {}

        list_buttons = ttk.Frame(list_frame, style="App.TFrame")
        list_buttons.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        ttk.Button(list_buttons, text="New Recipe", style="Primary.TButton", command=self.new_recipe).pack(side="left")
        ttk.Button(list_buttons, text="Edit", command=self.edit_selected_recipe).pack(side="left", padx=6)
        ttk.Button(list_buttons, text="Delete", style="Danger.TButton", command=self.delete_selected_recipe).pack(side="left")

        self.details_frame = ttk.Frame(content, style="App.TFrame", padding=(18, 0, 0, 0))
        self.details_frame.grid(row=1, column=1, sticky="nsew")
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(5, weight=1)
        self._build_details_panel()

    def _build_details_panel(self) -> None:
        self.detail_name = ttk.Label(self.details_frame, text="Select a recipe", font=("Segoe UI", 19, "bold"), background=self.CREAM, foreground=self.INK)
        self.detail_name.grid(row=0, column=0, sticky="w")
        self.detail_meta = ttk.Label(self.details_frame, text="", style="Muted.TLabel")
        self.detail_meta.grid(row=1, column=0, sticky="w", pady=(4, 18))
        ttk.Label(self.details_frame, text="Ingredients", style="Section.TLabel").grid(row=2, column=0, sticky="w")
        self.detail_ingredients = tk.Text(self.details_frame, height=7, wrap="word", state="disabled", relief="flat", background=self.WHITE, foreground=self.INK, padx=14, pady=10, font=("Segoe UI", 10), highlightthickness=1, highlightbackground=self.CREAM_DARK)
        self.detail_ingredients.grid(row=3, column=0, sticky="ew", pady=(6, 16))
        ttk.Label(self.details_frame, text="Instructions", style="Section.TLabel").grid(row=4, column=0, sticky="nw")
        self.detail_instructions = tk.Text(self.details_frame, wrap="word", state="disabled", relief="flat", background=self.WHITE, foreground=self.INK, padx=14, pady=10, font=("Segoe UI", 10), highlightthickness=1, highlightbackground=self.CREAM_DARK)
        self.detail_instructions.grid(row=5, column=0, sticky="nsew", pady=(6, 0))

    def refresh_recipe_list(self) -> None:
        for card in self.cards_container.winfo_children():
            card.destroy()
        self.card_widgets.clear()
        recipes = self.database.list_recipes(self.search_var.get())
        for index, recipe in enumerate(recipes):
            self._create_recipe_card(recipe, index)
        self.cards_canvas.yview_moveto(0)
        self.clear_details()

    def _create_recipe_card(self, recipe, index: int) -> None:
        card_background = self.WHITE if index % 2 == 0 else "#EDF4F5"
        card = tk.Frame(self.cards_container, background=card_background, highlightthickness=1, highlightbackground="#D7E4E6", padx=16, pady=13, cursor="hand2")
        card.pack(fill="x", padx=(2, 8), pady=(0, 9))
        card.columnconfigure(0, weight=1)
        name = tk.Label(card, text=recipe["name"], background=card_background, foreground=self.NAVY, font=("Segoe UI", 12, "bold"), anchor="w")
        name.grid(row=0, column=0, sticky="ew")
        meta = tk.Label(card, text=f"{recipe['prep_time']} min   •   {recipe['servings']} servings", background=card_background, foreground=self.MUTED, font=("Segoe UI", 9), anchor="w")
        meta.grid(row=1, column=0, sticky="ew", pady=(4, 0))
        self.card_widgets[recipe["recipe_id"]] = card
        for widget in (card, name, meta):
            widget.bind("<Button-1>", lambda _event, rid=recipe["recipe_id"]: self.select_recipe_card(rid))

    def select_recipe_card(self, recipe_id: int) -> None:
        self._highlight_card(recipe_id)
        self.show_recipe(recipe_id)

    def _highlight_card(self, recipe_id: int | None) -> None:
        for card_id, card in self.card_widgets.items():
            card.configure(highlightbackground=self.SAGE if card_id == recipe_id else "#D7E4E6", highlightthickness=2 if card_id == recipe_id else 1)

    def clear_search(self) -> None:
        self.search_var.set("")
        self.refresh_recipe_list()

    def clear_details(self) -> None:
        self.selected_recipe_id = None
        self._highlight_card(None)
        self.detail_name.configure(text="Select a recipe")
        self.detail_meta.configure(text="")
        self._set_text(self.detail_ingredients, "")
        self._set_text(self.detail_instructions, "")

    def show_selected_recipe(self, _event=None) -> None:
        return

    def show_recipe(self, recipe_id: int) -> None:
        recipe = self.database.get_recipe(recipe_id)
        if recipe is None:
            return
        self.selected_recipe_id = recipe_id
        self._highlight_card(recipe_id)
        self.detail_name.configure(text=recipe["name"])
        self.detail_meta.configure(text=f"{recipe['prep_time']} minutes  •  {recipe['servings']} servings")
        ingredients = "\n".join(f"• {item['quantity']} {item['unit']} {item['name']}" for item in recipe["ingredients"])
        self._set_text(self.detail_ingredients, ingredients)
        self._set_text(self.detail_instructions, recipe["instructions"])

    @staticmethod
    def _set_text(widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def new_recipe(self) -> None:
        self.open_recipe_editor()

    def edit_selected_recipe(self) -> None:
        if self.selected_recipe_id is None:
            messagebox.showinfo("Select a recipe", "Choose a recipe to edit first.")
            return
        self.open_recipe_editor(self.selected_recipe_id)

    def open_recipe_editor(self, recipe_id: int | None = None) -> None:
        editor = tk.Toplevel(self)
        editor.title("Edit Recipe" if recipe_id else "New Recipe")
        editor.geometry("650x650")
        editor.minsize(600, 550)
        editor.transient(self)
        editor.grab_set()
        editor.columnconfigure(1, weight=1)
        editor.rowconfigure(5, weight=1)
        editor.configure(bg=self.CREAM)
        frame = ttk.Frame(editor, padding=24, style="App.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        recipe = self.database.get_recipe(recipe_id) if recipe_id else None
        name_var = tk.StringVar(value=recipe["name"] if recipe else "")
        time_var = tk.StringVar(value=str(recipe["prep_time"]) if recipe else "")
        servings_var = tk.StringVar(value=str(recipe["servings"]) if recipe else "")
        ttk.Label(frame, text="Recipe name").grid(row=0, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=name_var).grid(row=0, column=1, sticky="ew", pady=6)
        ttk.Label(frame, text="Prep time (minutes)").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=time_var, width=12).grid(row=1, column=1, sticky="w", pady=6)
        ttk.Label(frame, text="Servings").grid(row=2, column=0, sticky="w", pady=6)
        ttk.Entry(frame, textvariable=servings_var, width=12).grid(row=2, column=1, sticky="w", pady=6)
        ttk.Label(frame, text="Ingredients").grid(row=3, column=0, columnspan=2, sticky="w", pady=(18, 5))

        ingredients_frame = ttk.Frame(frame, style="App.TFrame")
        ingredients_frame.grid(row=4, column=0, columnspan=2, sticky="nsew")
        ingredients_frame.columnconfigure(2, weight=1)
        ingredient_rows: list[tuple[ttk.Entry, ttk.Entry, ttk.Entry]] = []

        def add_ingredient_row(values: tuple[str, str, str] = ("", "", "")) -> None:
            row = len(ingredient_rows)
            quantity = ttk.Entry(ingredients_frame, width=10)
            unit = ttk.Entry(ingredients_frame, width=12)
            ingredient = ttk.Entry(ingredients_frame)
            quantity.grid(row=row, column=0, padx=(0, 5), pady=3)
            unit.grid(row=row, column=1, padx=(0, 5), pady=3)
            ingredient.grid(row=row, column=2, sticky="ew", pady=3)
            quantity.insert(0, values[0])
            unit.insert(0, values[1])
            ingredient.insert(0, values[2])
            ingredient_rows.append((quantity, unit, ingredient))

        ttk.Label(ingredients_frame, text="Quantity").grid(row=0, column=0, sticky="w")
        ttk.Label(ingredients_frame, text="Unit").grid(row=0, column=1, sticky="w")
        ttk.Label(ingredients_frame, text="Ingredient").grid(row=0, column=2, sticky="w")
        ingredients_frame.rowconfigure(1, weight=1)
        if recipe and recipe["ingredients"]:
            for item in recipe["ingredients"]:
                add_ingredient_row((item["quantity"], item["unit"], item["name"]))
        else:
            add_ingredient_row()

        ttk.Button(frame, text="Add ingredient", command=add_ingredient_row).grid(row=5, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Label(frame, text="Instructions").grid(row=6, column=0, columnspan=2, sticky="w", pady=(12, 5))
        instructions = tk.Text(frame, height=7, wrap="word", font=("Segoe UI", 10), background=self.WHITE, foreground=self.INK, insertbackground=self.INK, highlightthickness=1, highlightbackground=self.CREAM_DARK, padx=10, pady=8)
        instructions.grid(row=7, column=0, columnspan=2, sticky="nsew")
        if recipe:
            instructions.insert("1.0", recipe["instructions"])

        def save() -> None:
            try:
                name = name_var.get().strip()
                instructions_text = instructions.get("1.0", "end").strip()
                prep_time = int(time_var.get().strip())
                servings = int(servings_var.get().strip())
                if not name or not instructions_text:
                    raise ValueError("Recipe name and instructions are required.")
                if prep_time <= 0 or servings <= 0:
                    raise ValueError("Prep time and servings must be positive numbers.")
                ingredient_values = []
                for quantity_entry, unit_entry, ingredient_entry in ingredient_rows:
                    quantity = quantity_entry.get().strip()
                    unit = unit_entry.get().strip()
                    ingredient_name = ingredient_entry.get().strip()
                    if not quantity and not unit and not ingredient_name:
                        continue
                    if not quantity or not unit or not ingredient_name:
                        raise ValueError("Complete every ingredient row or leave it blank.")
                    ingredient_values.append({"quantity": quantity, "unit": unit, "name": ingredient_name})
                if not ingredient_values:
                    raise ValueError("Add at least one ingredient.")
                self.database.save_recipe(name, prep_time, servings, instructions_text, ingredient_values, recipe_id)
            except ValueError as error:
                messagebox.showerror("Invalid recipe", str(error), parent=editor)
                return
            except sqlite3.IntegrityError:
                messagebox.showerror("Duplicate recipe", "A recipe with that name already exists.", parent=editor)
                return
            editor.destroy()
            self.refresh_recipe_list()

        buttons = ttk.Frame(frame)
        buttons.grid(row=8, column=0, columnspan=2, sticky="e", pady=(15, 0))
        ttk.Button(buttons, text="Cancel", command=editor.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save Recipe", style="Primary.TButton", command=save).pack(side="right")

    def delete_selected_recipe(self) -> None:
        if self.selected_recipe_id is None:
            messagebox.showinfo("Select a recipe", "Choose a recipe to delete first.")
            return
        recipe = self.database.get_recipe(self.selected_recipe_id)
        if recipe and messagebox.askyesno("Delete recipe", f"Delete '{recipe['name']}'? This cannot be undone."):
            self.database.delete_recipe(self.selected_recipe_id)
            self.refresh_recipe_list()


if __name__ == "__main__":
    RecipeApp().mainloop()
