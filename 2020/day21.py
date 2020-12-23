import re
import numpy as np

def attribute_allergens(all_allergens):
    attributions = {}
    updates = True
    while len(attributions.keys())<len(all_allergens.keys()) and updates:
        updates = False
        for allergen in all_allergens.keys():
            if allergen not in attributions.keys():
                l = [ingr for ingr in all_allergens[allergen] if ingr not in attributions.values()]
                all_allergens[allergen] = l
                if len(l)==1:
                    attributions[allergen] = l[0]
                    updates = True

        # print(attributions)
        # input('Continue?')
    return attributions

def get_safe_ingredients(all_ingredients, all_allergens):
    safe_ingredients = []
    for ingr in np.unique(all_ingredients):
        absent = True
        for allergen, potential_ingredients in all_allergens.items():
            if ingr in potential_ingredients:
                absent = False
                continue
        if absent:
            safe_ingredients.append(ingr)
    return safe_ingredients


def count_allergens(all_ingredients, ingredients):
    c = 0
    for ingr in all_ingredients:
        c += ingr in ingredients
    return c

def question1():
    with open('inputs/day21.txt', 'r') as handle:
        lines = handle.readlines()
        lines = [l.strip('\n') for l in lines]

    input_list = []
    all_ingredients = []
    all_allergens = {}
    for l in lines:
        ingredients, allergens = l.split('(')
        ingredients = ingredients.split(' ')[:-1]
        all_ingredients += ingredients
        allergens = allergens.replace('contains ', '').strip(')').split(', ')
        input_list.append((ingredients, allergens))
        for aller in allergens:
            if aller not in all_allergens.keys():
                all_allergens[aller] = ingredients
            else:
                intersection = [ingr for ingr in all_allergens[aller] if ingr in ingredients]
                all_allergens[aller] = intersection


    attributions = attribute_allergens(all_allergens)
    safe_ingredients = get_safe_ingredients(all_ingredients, all_allergens)
    print(count_allergens(all_ingredients, safe_ingredients))


if __name__=="__main__":
    with open('inputs/day21.txt', 'r') as handle:
        lines = handle.readlines()
        lines = [l.strip('\n') for l in lines]

    input_list = []
    all_ingredients = []
    all_allergens = {}
    for l in lines:
        ingredients, allergens = l.split('(')
        ingredients = ingredients.split(' ')[:-1]
        all_ingredients += ingredients
        allergens = allergens.replace('contains ', '').strip(')').split(', ')
        input_list.append((ingredients, allergens))
        for aller in allergens:
            if aller not in all_allergens.keys():
                all_allergens[aller] = ingredients
            else:
                intersection = [ingr for ingr in all_allergens[aller] if ingr in ingredients]
                all_allergens[aller] = intersection


    attributions = attribute_allergens(all_allergens)
    answer = []
    for key in sorted(attributions.keys()):
        answer.append(attributions[key])

    print(','.join(answer))
