SHELL := /bin/bash
.PHONY: p v vulture pycodestyle mypy cleanall help

default:
	$(MAKE) p

help:
	@ echo "    p:           pylint"
	@ echo "    v:           vulture"
    @ echo "    vulture:     vulture with whitelist and statistics
	@ echo "    mypy:        mypy"
	@ echo "    pycodestyle: pycodestyle"

SOURCES=sortjscpd.py

p:
	pylint --extension-pkg-whitelist=cv2  $(SOURCES)
	@echo

v:
	vulture $(SOURCES)

cleanall:
	rm *.bak

# pip install pycodestyle
pycodestyle:
	pycodestyle --show-source  $(SOURCES)
	# or --show-pep8

# pip install vulture and $(MAKE) vulturesetup
vulture:
	vulture $(SOURCES) whitelist.py | tee /tmp/vulture_output.txt; echo -n "Number of issues: "; wc -l < /tmp/vulture_output.txt

vulturesetup:
	- vulture $(SOURCES) --make-whitelist > whitelistnew.py
	if [ -f whitelist.py ]; then \
		diff <(cut -d '#' -f 1 whitelist.py | sed 's/[[:space:]]*$$//') \
			<(cut -d '#' -f 1 whitelistnew.py | sed 's/[[:space:]]*$$//'); \
  	fi
	@echo "edit whitelistnew.py and replace whitelist.py"


# pip install mypy
mypy:
	export MYPYPATH=out;mypy $(SOURCES)