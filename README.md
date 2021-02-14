# RandomMeals

## Getting Started

### Prerequisites

* Python 3.6 (with [Anaconda](https://docs.anaconda.com/anaconda/install/windows/) to get project environment).

### Installing

Using Anaconda Prompt (or cmd if you set Anaconda PATH during the Anaconda installation) :
 
* Create the environment for the project and install the requirements by running the following commands: 
```
conda create --name py36_random_meals_env python=3.6
conda activate py36_random_meals_env
pip install -r requirements.txt
```
* or simply run the file [install_random_meals.bat](install_random_meals.bat)

### Filling the recipes data

Set all of your recipes data in [data/recipes.json](data/recipes.json) using the following format :
```
{
    "name_recipe": "<name of your recipe>",
    "ingredients": [
      {
        "name": "<name of the first ingredient - required>",
        "quantity": <quantity of this ingredient relatively to the unit - required>,
        "unit": "<optional>"
      },
      ...
      <next ingredient>
      ...
	  {
        "name": "<name of the last ingredient - required>",
        "quantity": <quantity - required>,
        "unit": "<optional>"
      }
    ]
},
...
<next recipe>
```

Example :
```
{
    "name_recipe": "pates sauce tomate",
    "ingredients": [
      {
        "name": "pates",
        "quantity": 100,
        "unit": "g"
      },
      {
        "name": "tomates",
        "quantity": 100,
        "unit": "g"
      }
      {
        "name": "tomates",
        "quantity": 3,
      }
    ]
},
```

### Generating shopping list

* To generate the random meals of the week and the associated shopping list,
run the file [generate_random_meals.bat](generate_random_meals.bat). It will create
  a pdf, located in [data/shopping_list.pdf](data/shopping_list.pdf).

## Further improvements
* generate output user as google keep [link](https://github.com/kiwiz/gkeepapi)