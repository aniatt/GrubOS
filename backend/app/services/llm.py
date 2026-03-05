from collections.abc import AsyncGenerator

import ollama

MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """\
You are a creative and practical home chef. Given a list of available ingredients, \
generate delicious, realistic recipes that primarily use those ingredients. \
You may assume the user has basic pantry staples (salt, pepper, oil, butter, sugar, flour, garlic). \
For each recipe, provide: a title, a brief description, the ingredient list with quantities, \
and numbered step-by-step instructions. Keep instructions concise and beginner-friendly.\
"""


def _build_user_prompt(
    ingredients: list[str],
    num_recipes: int,
    cuisine: str | None,
    dietary_restrictions: list[str],
    max_cooking_minutes: int | None,
) -> str:
    parts = [f"I have these ingredients: {', '.join(ingredients)}."]
    parts.append(f"Please suggest {num_recipes} recipe(s).")

    if cuisine:
        parts.append(f"Cuisine preference: {cuisine}.")
    if dietary_restrictions:
        parts.append(f"Dietary restrictions: {', '.join(dietary_restrictions)}.")
    if max_cooking_minutes:
        parts.append(f"Max cooking time: {max_cooking_minutes} minutes.")

    return " ".join(parts)


class LLMService:
    def __init__(self, model: str = MODEL):
        self.model = model
        self._client = ollama.Client()

    async def check_connection(self) -> bool:
        try:
            self._client.list()
            return True
        except Exception:
            return False

    async def generate_recipes_stream(
        self,
        ingredients: list[str],
        num_recipes: int = 2,
        cuisine: str | None = None,
        dietary_restrictions: list[str] | None = None,
        max_cooking_minutes: int | None = None,
    ) -> AsyncGenerator[str, None]:
        user_prompt = _build_user_prompt(
            ingredients=ingredients,
            num_recipes=num_recipes,
            cuisine=cuisine,
            dietary_restrictions=dietary_restrictions or [],
            max_cooking_minutes=max_cooking_minutes,
        )

        stream = self._client.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
        )

        for chunk in stream:
            token = chunk["message"]["content"]
            if token:
                yield token


llm_service = LLMService()
