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
    nb_of_recipes_to_choose = 3

    logger.debug('Beginning of program')
    list_recipes = return_content_json_file('data/recipes.json')

    # choose the recipe for the week
    chosen_recipes = random.sample(list_recipes, k=min(nb_of_recipes_to_choose, len(list_recipes)))
    chosen_recipes_names = [chosen_recipe['name_recipe'] for chosen_recipe in chosen_recipes]

    # output the chosen recipes of the week
    write_json_file('data/chosen_recipes.json', chosen_recipes_names)

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
    write_pdf_file('data/shopping_list.pdf', chosen_recipes_names, shopping_list)
