import pathlib
import sys
import os
import parse as scanf


def parse(puzzle_input):
    """Parse input"""
    lines = []
    for line in puzzle_input.split('\n'):
        ingredients_str, allergens_str = scanf.parse('{} (contains {})', line)
        ingredients = set(ingredients_str.split())
        allergens = set(allergens_str.split(', '))
        lines.append((ingredients, allergens))
    return lines


def determine_allergens(ingredient_list: list[set[str]], allergen_list: list[set[str]]) -> dict[str, str]:
    translation: dict[str, str] = {}
    remaining: set[str] = allergen_list[0].copy()
    completed: set[str] = set()
    potentials: dict[str, set[str]] = {}

    while remaining:
        for i, ingredients1 in enumerate(ingredient_list):
            uncompleted_allergens: set[str] = allergen_list[i] - completed
            untranslated_ingredients: set[str] = ingredients1 - translation.keys()

            if len(uncompleted_allergens) == len(untranslated_ingredients) == 1:
                ingredient: str = untranslated_ingredients.pop()
                allergen: str = uncompleted_allergens.pop()
                remaining.discard(allergen)
                completed.add(allergen)
                translation[ingredient] = allergen
                if allergen in potentials:
                    del potentials[allergen]
            else:
                remaining.update(uncompleted_allergens)

            for j, ingredients2 in enumerate(ingredient_list[i + 1:], i + 1):
                for allergen in (allergen_list[i] & allergen_list[j]) - completed:
                    potential_ingredients: set[str] = (ingredients1 & ingredients2) - translation.keys()
                    if allergen in potentials:
                        potentials[allergen] &= potential_ingredients
                    elif potential_ingredients:
                        potentials[allergen] = potential_ingredients

                    if len(potentials.get(allergen, set())) == 1:
                        ingredient: str = potentials[allergen].pop()
                        remaining.discard(allergen)
                        completed.add(allergen)
                        translation[ingredient] = allergen
                        del potentials[allergen]
    return translation


def part1(data):
    """Solve part 1"""
    ingredient_list = [ingredients for ingredients, allergens in data]
    allergen_list = [allergens for ingredients, allergens in data]

    translation: dict[str, str] = determine_allergens(ingredient_list, allergen_list)

    non_allergenic: int = 0
    for ingredients in ingredient_list:
        for ingredient in ingredients:
            if ingredient not in translation:
                non_allergenic += 1
    return non_allergenic


def part2(data):
    """Solve part 2"""
    ingredient_list = [ingredients for ingredients, allergens in data]
    allergen_list = [allergens for ingredients, allergens in data]

    translation: dict[str, str] = determine_allergens(ingredient_list, allergen_list)
    translation_pairs: list[tuple[str, str]] = [(allergen, ingredient) for ingredient, allergen in translation.items()]
    dangerous_ingredients: list[str] = [ingredient for _, ingredient in sorted(translation_pairs)]
    return ','.join(dangerous_ingredients)


def solve(puzzle_input):
    """Solve the puzzle for the given input"""
    data = parse(puzzle_input)
    solution1 = part1(data)
    data = parse(puzzle_input)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    DIR = f'{os.path.dirname(sys.argv[0])}/'
    for file in ('example.txt', 'input.txt'):
        print(f"{file}:")
        puzzle_input = pathlib.Path(DIR + file).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))
        print()
