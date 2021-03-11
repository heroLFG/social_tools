
build:
	docker build -t my-golang-app .

run:
	-docker rm my-running-app
	docker run -v $(PWD)/src:/go/src/app -p 127.0.0.1:8080:8080 -it --rm --name my-running-app my-golang-app

test:
	echo $(PWD)
