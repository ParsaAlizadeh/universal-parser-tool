.PHONY: install build uninstall clean clean-dist
install: uninstall build
	sudo pip install dist/*.whl
build: clean-dist
	python setup.py bdist_wheel
uninstall:
	yes | sudo pip uninstall universal-parser-tool
clean:
	rm -rf build/ *egg*/
clean-dist:
	rm -rf dist/