# RandomMeals

## Getting Started

### Prerequisites

* Python 3.6 (with Anaconda to get project environment).

### Installing

* Create the environment for the project and install the requirements by running the following commands: 
```
conda create --name py36_random_meals_env python=3.6
conda activate py36_random_meals_env
pip install -r requirements.txt
```
or simply run the file [install_random_meals.bat](install_random_meals.bat)

### Generating shopping list
* To generate the random meals of the week and the associated shopping list,
run the file [generate_random_meals.bat](generate_random_meals.bat). It will create
  a pdf, located in [data/shopping_list.pdf](data/shopping_list.pdf).

## TO DO
* generate as google keep [link](https://github.com/kiwiz/gkeepapi)