mig:
	py manage.py makemigrations
	py manage.py migrate
run:
	py manage.py runserver
runp:
	py manage.py runserver 0.0.0.0:8000

user:
	py manage.py createsuperuser