REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/genome-browser/front-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/genome-browser/front-web/test .
	sudo docker tag genopedia/genome-browser/front-web/test $(REGISTRY)/genopedia/genome-browser/front-web/test
	sudo docker push $(REGISTRY)/genopedia/genome-browser/front-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/genome-browser/front-web/prod .
	sudo docker tag genopedia/genome-browser/front-web/prod $(REGISTRY)/genopedia/genome-browser/front-web/prod
	sudo docker push $(REGISTRY)/genopedia/genome-browser/front-web/prod
