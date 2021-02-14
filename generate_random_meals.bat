@echo OFF
call conda activate py36_random_meals_env
python src/main.py
call conda deactivate
echo SHOPPING LIST HAS BEEN CREATED. ENJOY!