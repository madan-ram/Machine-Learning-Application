install:
	mysql -u root -p -e "create database twitbird;"
	sudo python manage.py syncdb
	sudo python manage.py runserver