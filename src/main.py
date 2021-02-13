import json
import random

import fpdf

from utils.logger import logger


def return_content_json_file(path_file):
    with open(path_file) as json_file:
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
    if isinstance(checkbox_content_subpart, list):
        # list = chosen recipes
        for recipe in checkbox_content_subpart:
            pdf_file.write(5, '☐ {}'.format(recipe))
            pdf_file.ln()
    elif isinstance(checkbox_content_subpart, dict):
        # dict = shopping list
        for key, quantity in checkbox_content_subpart.items():
            checkbox_line = '☐ {} ({}{})'.format(key[0], quantity, key[1]) if isinstance(key, tuple) \
                else '☐ {} ({})'.format(key, quantity)

            pdf_file.write(5, checkbox_line)
            pdf_file.ln()

    return pdf_file


def write_pdf_file(path_file, chosen_recipes_names, shopping_list):
    pdf_file = fpdf.FPDF(format='A4')
    pdf_file.add_page()
    pdf_file.add_font('DejaVu', '', 'src/pdf_utils/DejaVuSansCondensed.ttf', uni=True)

    write_subpart_pdf(pdf_file, 'LISTE DE RECETTES DE LA SEMAINE', chosen_recipes_names)
    pdf_file.ln()
    write_subpart_pdf(pdf_file, 'LISTE DE COURSES POUR LA SEMAINE', shopping_list)

    pdf_file.output(path_file)


if __name__ == '__main__':
    nb_of_recipes_to_choose = 2

    logger.debug('Beginning of program')
    list_recipes = return_content_json_file('data/recipes.json')

    # get recipes of last week
    chosen_recipes_names_last_week = set(return_content_json_file('data/chosen_recipes.json'))
    logger.debug('Recipes of last week: {}'.format(chosen_recipes_names_last_week))

    # choose the recipes for the week
    # 1. take recipes which were not selected last week
    all_recipes_names = set([recipe['name_recipe'] for recipe in list_recipes])
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
            ingredient_unit = ingredient_recipe.get('unit', None)

            logger.debug('Ingredient "{}" will be added to the shopping list (for recipe "{}")'.format(ingredient_name,
                                                                                                       recipe[
                                                                                                           'name_recipe']))

            key = (ingredient_name, ingredient_unit.lower()) if ingredient_unit is not None else ingredient_name
            shopping_list[key] = shopping_list.get(key, 0) + ingredient_quantity
    logger.debug('Shopping list: {}'.format(shopping_list))

    # generate the output for user
    logger.debug('Write output pdf')
    write_pdf_file('data/shopping_list.pdf', chosen_recipes_names, shopping_list)

    logger.debug('End of program')