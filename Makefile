.PHONY: all venv run clean

# default target, when make executed without arguments
all: install

$(VENV)/bin/activate: setup.py
	pyenv virtualenv 3.8.5 ghd
	pyenv activate ghd
	pip install --upgrade pip

install: groundhogs_day
	pip3 install -e .

uninstall:
	pip3 uninstall ghd -y

# venv is a shortcut target
venv: $(VENV)/bin/activate

run: venv
	#./$(VENV)/bin/python3 app.py
	ghd

test: install
# 	ghd list organization --output table
# 	ghd list organization --output json
# 	ghd list organization --output json --export
# 	ghd list accounts --output table
# 	ghd list accounts --output csv
# 	ghd list accounts --output json	
# 	ghd list accounts --output csv --export
# 	ghd list accounts --output json	--export
# 	ghd list org_admins --output table
# 	ghd list org_admins --output json
# 	ghd list org_admins --output json --export
	ghd s3account --off
	ghd s3account --on

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete