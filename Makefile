.PHONY: install build uninstall clean clean-dist
install: uninstall
	sudo python setup.py install
build: clean-dist
	python setup.py bdist_wheel
uninstall:
	yes | sudo pip uninstall universal-parser-tool
clean:
	rm -rf build/ *egg*/
clean-dist:
	rm -rf dist/
