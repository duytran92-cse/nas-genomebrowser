GENOME_BROWSER_API_MYSQL_HOST_PORT=3303
GENOME_BROWSER_API_WEB_HOST_PORT=8003
GENOME_BROWSER_ADMIN_MYSQL_HOST_PORT=3304
GENOME_BROWSER_ADMIN_WEB_HOST_PORT=8004
GENOME_BROWSER_FRONT_MYSQL_HOST_PORT=3305
GENOME_BROWSER_FRONT_WEB_HOST_PORT=8005
GENOME_BROWSER_API_RABBITMQ_HOST_PORT=5700
GENOME_BROWSER_API_RABBITMQ_ADMIN_HOST_PORT=15600
GENOPEDIA_GENOME_BROWSER_HOME=$(GENOPEDIA_HOME)/genopedia-genome-browser

create-storage:
	sudo docker run -d --name=genopedia-dev.genome-browser-api.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=genopedia-dev.genome-browser-admin.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true
	sudo docker run -d --name=genopedia-dev.genome-browser-front.mysql.storage \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1 true

clear-storage:
	-sudo docker stop genopedia-dev.genome-browser-api.mysql.storage
	-sudo docker rm genopedia-dev.genome-browser-api.mysql.storage
	-sudo docker stop genopedia-dev.genome-browser-admin.mysql.storage
	-sudo docker rm genopedia-dev.genome-browser-admin.mysql.storage
	-sudo docker stop genopedia-dev.genome-browser-front.mysql.storage
	-sudo docker rm genopedia-dev.genome-browser-front.mysql.storage

deploy:
	sudo docker run -d --name=genopedia-dev.genome-browser-api.rabbitmq \
		-p $(GENOME_BROWSER_API_RABBITMQ_HOST_PORT):5672 \
		-p $(GENOME_BROWSER_API_RABBITMQ_ADMIN_HOST_PORT):15672 \
		registry.novogenialab.com/notasquare-zero/images/standard-rabbitmq:0.1
	sudo docker run -d --name=genopedia-dev.genome-browser-api.mysql \
		--volumes-from=genopedia-dev.genome-browser-api.mysql.storage \
		-p $(GENOME_BROWSER_API_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.genome-browser-api.web \
		--link genopedia-dev.genome-browser-api.mysql:mysql \
		--link genopedia-dev.genome-browser-api.rabbitmq:rabbitmq \
		-v $(GENOPEDIA_GENOME_BROWSER_HOME)/api-web/src/www:/opt/www \
		-p $(GENOME_BROWSER_API_WEB_HOST_PORT):80 \
		genopedia/genome-browser/api-web/dev

	sudo docker run -d --name=genopedia-dev.genome-browser-admin.mysql \
		-p $(GENOME_BROWSER_ADMIN_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.genome-browser-admin.web \
		--link genopedia-dev.genome-browser-admin.mysql:mysql \
		--link genopedia-dev.genome-browser-api.web:genome-browser-api \
		-v $(GENOPEDIA_GENOME_BROWSER_HOME)/admin-web/src/www:/opt/www \
		-p $(GENOME_BROWSER_ADMIN_WEB_HOST_PORT):80 \
		genopedia/genome-browser/admin-web/dev

	sudo docker run -d --name=genopedia-dev.genome-browser-front.mysql \
		-p $(GENOME_BROWSER_FRONT_MYSQL_HOST_PORT):3306 \
		registry.novogenialab.com/notasquare-zero/images/standard-mysql:0.1
	sudo docker run -d --name=genopedia-dev.genome-browser-front.web \
		--link genopedia-dev.genome-browser-front.mysql:mysql \
		--link genopedia-dev.genome-browser-api.web:genome-browser-api \
		--link genopedia-dev.user-api.web:user-api \
		-v $(GENOPEDIA_GENOME_BROWSER_HOME)/front-web/src/www:/opt/www \
		-p $(GENOME_BROWSER_FRONT_WEB_HOST_PORT):80 \
		genopedia/genome-browser/front-web/dev

	sudo cp nginx/genopedia-genome-browser-api-rabbitmq /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-genome-browser-api-web /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-genome-browser-admin-web /etc/nginx/sites-enabled
	sudo cp nginx/genopedia-genome-browser-front-web /etc/nginx/sites-enabled
	sudo service nginx reload

	sleep 10

	-sudo docker exec -it genopedia-dev.genome-browser-api.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS api_db;"
	-sudo docker exec -it genopedia-dev.genome-browser-api.web python /opt/www/manage.py migrate

	-sudo docker exec -it genopedia-dev.genome-browser-admin.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS admin_db;"
	-sudo docker exec -it genopedia-dev.genome-browser-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genome-browser-admin.web python /opt/www/manage.py linkstatic

	-sudo docker exec -it genopedia-dev.genome-browser-front.mysql mysql -uroot -p123456 -e "CREATE DATABASE IF NOT EXISTS front_db;"
	-sudo docker exec -it genopedia-dev.genome-browser-front.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genome-browser-front.web python /opt/www/manage.py linkstatic

clean:
	-sudo docker stop genopedia-dev.genome-browser-admin.mysql
	-sudo docker stop genopedia-dev.genome-browser-admin.web
	-sudo docker stop genopedia-dev.genome-browser-front.mysql
	-sudo docker stop genopedia-dev.genome-browser-front.web
	-sudo docker stop genopedia-dev.genome-browser-api.mysql
	-sudo docker stop genopedia-dev.genome-browser-api.rabbitmq
	-sudo docker stop genopedia-dev.genome-browser-api.web

	-sudo docker rm genopedia-dev.genome-browser-admin.mysql
	-sudo docker rm genopedia-dev.genome-browser-admin.web
	-sudo docker rm genopedia-dev.genome-browser-front.mysql
	-sudo docker rm genopedia-dev.genome-browser-front.web
	-sudo docker rm genopedia-dev.genome-browser-api.mysql
	-sudo docker rm genopedia-dev.genome-browser-api.rabbitmq
	-sudo docker rm genopedia-dev.genome-browser-api.web

	-sudo rm /etc/nginx/sites-enabled/genopedia-genome-browser-api-web
	-sudo rm /etc/nginx/sites-enabled/genopedia-genome-browser-api-rabbitmq
	-sudo rm /etc/nginx/sites-enabled/genopedia-genome-browser-admin-web
	-sudo rm /etc/nginx/sites-enabled/genopedia-genome-browser-front-web

start:
	sudo docker start genopedia-dev.genome-browser-api.rabbitmq
	sudo docker start genopedia-dev.genome-browser-api.mysql
	sudo docker start genopedia-dev.genome-browser-api.web
	sudo docker start genopedia-dev.genome-browser-admin.mysql
	sudo docker start genopedia-dev.genome-browser-admin.web
	sudo docker start genopedia-dev.genome-browser-front.mysql
	sudo docker start genopedia-dev.genome-browser-front.web

stop:
	sudo docker stop genopedia-dev.genome-browser-api.rabbitmq
	sudo docker stop genopedia-dev.genome-browser-api.mysql
	sudo docker stop genopedia-dev.genome-browser-api.web
	sudo docker stop genopedia-dev.genome-browser-admin.mysql
	sudo docker stop genopedia-dev.genome-browser-admin.web
	sudo docker stop genopedia-dev.genome-browser-front.mysql
	sudo docker stop genopedia-dev.genome-browser-front.web

migrate:
	-sudo docker exec -it genopedia-dev.genome-browser-api.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genome-browser-admin.web python /opt/www/manage.py migrate
	-sudo docker exec -it genopedia-dev.genome-browser-front.web python /opt/www/manage.py migrate

ssh-api-mysql:
	sudo docker exec -it genopedia-dev.genome-browser-api.mysql bash
ssh-api-rabbitmq:
	sudo docker exec -it genopedia-dev.genome-browser-api.rabbitmq bash
ssh-api-web:
	sudo docker exec -it genopedia-dev.genome-browser-api.web bash

ssh-admin-mysql:
	sudo docker exec -it genopedia-dev.genome-browser-admin.mysql bash

ssh-admin-web:
	sudo docker exec -it genopedia-dev.genome-browser-admin.web bash

ssh-front-mysql:
	sudo docker exec -it genopedia-dev.genome-browser-front.mysql bash

ssh-front-web:
	sudo docker exec -it genopedia-dev.genome-browser-front.web bash
