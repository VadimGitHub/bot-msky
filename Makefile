#######################################################################################################################
# pip
#######################################################################################################################
freeze: ## Сохранение зависимостей
	pip freeze > requirements.txt

install: ## Установка зависимостей
	pip install -r requirements.txt
