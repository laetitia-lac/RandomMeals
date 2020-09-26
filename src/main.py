import pandas as pd

from utils.logger import logger

if __name__ == '__main__':
    nb_of_recipes_to_choose = 2

    logger.debug('beginning programm')
    df = pd.read_csv('data/list_recipes.csv', sep=";")
    logger.debug('columns : ' + df.columns)

    # choose the recipe for the week
    recipes = df['name_recipe'].dropna()
    chosen_recipes = recipes.sample(nb_of_recipes_to_choose, replace=True)

    ## output the chosen recipes of the week
    chosen_recipes.to_csv('data/list_recipes_of_the_week.csv', index=False, header=False)

    # generate the shopping list

    ## get all the ingredients for the week
    ingredients = list()
    for index_start_recipe, recipe in chosen_recipes.iteritems():
        logger.debug("start to select ingredients of this recipe : " + recipe)
        current_index = index_start_recipe
        while current_index < len(df.index) and (df.loc[current_index, 'name_recipe'] is not None or df.loc[current_index, 'name_recipe'] == recipe):
            logger.debug("this ingredient {} for this recipe {} was taken".format(df.loc[current_index, 'name_ingredient'], recipe))
            ingredients.append(df.loc[current_index, 'name_ingredient'])
            current_index += 1
            logger.debug("end to select ingredients of this recipe : " + recipe)

    logger.debug("list of ingredients of the week" + str(ingredients))

