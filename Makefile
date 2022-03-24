python-dependencies:
	export LC_ALL=C.UTF-8
	export LANG=C.UTF-8
	-rm requirements.txt
	PIP_CONFIG_FILE=~/.pip/pip3.conf python3 -m piptools compile -v --rebuild --output-file requirements.txt requirements.in 
	git diff --quiet version.txt requirements.txt || git add version.txt requirements.txt && git commit -m "chg[ci-skip]: requirements.txt v`cat version.txt`" && git push origin master || (echo 1 && echo 2)