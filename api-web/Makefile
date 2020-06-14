REGISTRY=registry.novogenialab.com

build:
	sudo docker build -f docker/Dockerfile-dev -t genopedia/genome-browser/api-web/dev .

release-test:
	sudo docker build --no-cache -f docker/Dockerfile-test -t genopedia/genome-browser/api-web/test .
	sudo docker tag genopedia/genome-browser/api-web/test $(REGISTRY)/genopedia/genome-browser/api-web/test
	sudo docker push $(REGISTRY)/genopedia/genome-browser/api-web/test

release-prod:
	sudo docker build --no-cache -f docker/Dockerfile-prod -t genopedia/genome-browser/api-web/test .
	sudo docker tag genopedia/genome-browser/api-web/prod $(REGISTRY)/genopedia/genome-browser/api-web/prod
	sudo docker push $(REGISTRY)/genopedia/genome-browser/api-web/prod
