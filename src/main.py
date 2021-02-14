import json
import random

import fpdf

from utils.logger import logger


def return_content_json_file(path_file):
    with open(path_file, 'rb') as json_file:
        return json.load(json_file)


def write_json_file(path_file, content_json):
    with open(path_file, 'w') as json_file:
        json.dump(content_json, json_file)


def write_subpart_pdf(pdf_file, title_subpart, checkbox_content_subpart):
    # title subpart
    pdf_file.set_font('DejaVu', size=16)
    pdf_file.cell(40, 10, title_subpart)
    pdf_file.ln()

    # checkbox subpart
    pdf_file.set_font('DejaVu', size=12)
    for checkbox_line in checkbox_content_subpart:
        pdf_file.write(5, checkbox_line)
        pdf_file.ln()

    return pdf_file


def write_pdf_file(path_file, chosen_recipes_names, shopping_list):
    pdf_file = fpdf.FPDF(format='A4')
    pdf_file.add_page()
    pdf_file.add_font('DejaVu', '', 'src/pdf_utils/DejaVuSans.ttf', uni=True)

    write_subpart_pdf(pdf_file, 'LISTE DE RECETTES DE LA SEMAINE', chosen_recipes_names)
    pdf_file.ln()
    write_subpart_pdf(pdf_file, 'LISTE DE COURSES POUR LA SEMAINE', shopping_list)

    pdf_file.output(path_file)


if __name__ == '__main__':
    nb_of_recipes_to_choose = int(input('Indicate the number of meals to generate for this week: '))

    logger.debug('Beginning of program')
    list_recipes = return_content_json_file('data/recipes.json')

    # get recipes of last week
    chosen_recipes_names_last_week = set(return_content_json_file('data/chosen_recipes.json'))
    logger.debug('Recipes of last week: {}'.format(chosen_recipes_names_last_week))

    # choose the recipes for the week
    # 1. take recipes which were not selected last week
    all_recipes_names = {recipe['name_recipe'] for recipe in list_recipes}
    unused_recipes_names = all_recipes_names - chosen_recipes_names_last_week
    logger.debug('Unused recipes: {}'.format(unused_recipes_names))
    chosen_recipes_names = random.sample(unused_recipes_names,
                                         k=min(nb_of_recipes_to_choose, len(unused_recipes_names)))

    # 2. if needed, take chosen recipes from last week
    nb_missing_recipes = nb_of_recipes_to_choose - len(chosen_recipes_names)
    if nb_missing_recipes > 0:
        chosen_recipes_names.extend(
            random.sample(chosen_recipes_names_last_week,
                          k=min(nb_missing_recipes, len(chosen_recipes_names_last_week))))
    logger.debug('Recipes of the week: {}'.format(chosen_recipes_names))

    # output the chosen recipes of the week as json
    write_json_file('data/chosen_recipes.json', chosen_recipes_names)

    # get chosen recipes from the name
    chosen_recipes = [recipe for recipe in list_recipes if recipe['name_recipe'] in chosen_recipes_names]
    logger.debug('Recipes of the week (with list of ingredients): {}'.format(chosen_recipes))

    # generate the shopping list
    shopping_list = dict()
    for recipe in chosen_recipes:
        for ingredient_recipe in recipe['ingredients']:
            ingredient_name = ingredient_recipe['name'].lower()
            ingredient_quantity = ingredient_recipe['quantity']
            ingredient_unit = ingredient_recipe['unit'].lower() if ingredient_recipe.get('unit') else None

            logger.debug('Ingredient "{}" will be added to the shopping list (for recipe "{}")'.format(ingredient_name,
                                                                                                       recipe[
                                                                                                           'name_recipe']))

            # add ingredient to shopping list
            ingredient_dict = shopping_list.get(ingredient_name, dict())
            ingredient_dict[ingredient_unit] = ingredient_dict.get(ingredient_unit, 0) + ingredient_quantity
            shopping_list[ingredient_name] = ingredient_dict

    logger.debug('Shopping list: {}'.format(shopping_list))

    # generate the output for user
    # 1. format chosen recipes names
    formatted_chosen_recipes_names = ['☐ {}'.format(recipe) for recipe in chosen_recipes_names]
    # 2. format shopping list
    formatted_shopping_list = list()
    name_ingredients_sorted = sorted(shopping_list.keys())
    for name_ingredient in name_ingredients_sorted:
        for unit, quantity in shopping_list[name_ingredient].items():
            formatted_shopping_list.append('☐ {} ({}{})'.format(name_ingredient, quantity, unit) if unit is not None
                                           else '☐ {} ({})'.format(name_ingredient, quantity))

    logger.debug('Write output pdf')
    write_pdf_file('data/shopping_list.pdf', formatted_chosen_recipes_names, formatted_shopping_list)

    logger.debug('End of program')