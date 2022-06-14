all:
	@echo nothing special

lint:
	python3 -m mdk_tools.cli.py_lint .

prepare:
	python3 -m pip install -r requirements.txt --user

# install:
# 	@cp pre_commit.sh .git/hooks/pre-commit || true
# 	@python3 setup.py install --user

upload:
	python3 setup.py bdist_wheel upload -r local
package:clean prepare
	python3 setup.py bdist_wheel

install: package
	python3 -m pip install dist/*.whl -U --force-reinstall
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -f *.pyc

# DOCKER_BUILD_TAG := artifactory.momenta.works/docker-momenta/ubuntu1604-python36:v0.0.1
# docker_test_build:
# 	docker run --rm -v `pwd`:/workdir \
# 		-it $(DOCKER_BUILD_TAG) zsh

# DOCKER_RELEASE_TAG := artifactory.momenta.works/docker-momenta/smpy:v1.6.5
# docker_build:
# 	docker build --tag $(DOCKER_RELEASE_TAG) .
# docker_push:
# 	docker push $(DOCKER_RELEASE_TAG)
# docker_test_release:
# 	docker run --rm -v `pwd`:/workdir -it $(DOCKER_RELEASE_TAG) zsh
