# Copyright 2015,2016 Nir Cohen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Name of this package
PACKAGENAME = backtrace

# Default tox env when running `make testone`
TOX_ENV ?= py36


.PHONY: help
help:
	@echo 'Please use "make <target>" where <target> is one of'
	@echo "  release   - build a release and publish it"
	@echo "  dev       - prepare a development environment (includes tests)"
	@echo "  instdev   - prepare a development environment (no tests)"
	@echo "  install   - install into current Python environment"
	@echo "  build     - build the package"
	@echo "  test      - test from this directory using tox, including test coverage"
	@echo "  publish   - upload to PyPI"
	@echo "  clean     - remove any temporary build products"
	@echo "  dry-run   - perform all action required for a release without actually releasing"

.PHONY: release
release: test clean build publish
	@echo "$@ done."

.PHONY: test
test:
	pip install 'tox>=1.7.2'
	tox
	@echo "$@ done."

.PHONY: testone
testone:
	pip install 'tox>=1.7.2'
	tox -e $(TOX_ENV)
	@echo "$@ done."

.PHONY: clean
clean:
	rm -rf dist build $(PACKAGENAME).egg-info
	@echo "$@ done."

.PHONY: build
build:
	python setup.py sdist bdist_wheel

.PHONY: publish
publish:
	pip install twine
	twine upload -r pypi dist/$(PACKAGENAME)-*
	@echo "$@ done."

.PHONY: dry-run
dry-run: test clean build
	@echo "$@ done."

.PHONY: dev
dev: instdev test
	@echo "$@ done."

.PHONY: instdev
instdev:
	pip install -r dev-requirements.txt
	python setup.py develop
	@echo "$@ done."

.PHONY: install
install:
	python setup.py install
	@echo "$@ done."
