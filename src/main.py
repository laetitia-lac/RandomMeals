import json
import random

from utils.logger import logger


def return_content_json_file(path_file):
    with open(path_file) as json_file:
        return json.load(json_file)


def write_json_file(path_file, content_json):
    with open(path_file, 'w') as json_file:
        json.dump(content_json, json_file)


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
    ## get all the ingredients for the week
    shopping_list = dict()
    for recipe in chosen_recipes:
        for ingredient_recipe in recipe['ingredients']:
            ingredient_name = ingredient_recipe['name'].lower()
            ingredient_quantity = ingredient_recipe['quantity']

            logger.debug('Ingredient "{}" will be added to the shopping list (for recipe "{}")'.format(ingredient_name,
                                                                                                       recipe[
                                                                                                           'name_recipe']))

            shopping_list[ingredient_name] = shopping_list.get(ingredient_name, 0) + ingredient_quantity

    logger.debug('Shopping list: {}'.format(shopping_list))
