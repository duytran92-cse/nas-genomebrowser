REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/genome-browser/admin-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/genome-browser/admin-web/test .
	sudo docker tag genopedia/genome-browser/admin-web/test $(REGISTRY)/genopedia/genome-browser/admin-web/test
	sudo docker push $(REGISTRY)/genopedia/genome-browser/admin-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/genome-browser/admin-web/prod .
	sudo docker tag genopedia/genome-browser/admin-web/prod $(REGISTRY)/genopedia/genome-browser/admin-web/prod
	sudo docker push $(REGISTRY)/genopedia/genome-browser/admin-web/prod
