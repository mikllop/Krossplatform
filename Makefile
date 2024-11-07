PYTHON=python3
PYTHON_BSD_LIN=python3.12
PYINSTALLER=pyinstaller
FILE_NAME=wampus.py
WINDOWS_SOURCE=.\wampus.py
LINUX_SOURCE=`pwd`/wampus.py
BSD_SOURCE=./wampus.py
WINDOWS_OUTPUT=.\output\windows
LINUX_OUTPUT=`pwd`/output/linux
WINDOWS_OPTIONS=--onefile --console
LINUX_OPTIONS=--onefile --console
CLEANING_FILE=clear.py
BSD_PRE_PRE_FLAGS=LD_LIBRARY_PATH=/usr/pkg/include/python3.12/:/usr/pkg/lib/
BSD_PRE_FLAGS=-Os -I/usr/pkg/include/python3.12 -I/usr/pkg/include/python3.12 -L/usr/pkg/lib  -lintl -lpthread -lcrypt -lutil -lm

all: windows linux web

windows:
	pip install -r requirements.txt
	@echo "Building for Windows..."
	$(PYINSTALLER) $(WINDOWS_OPTIONS) $(WINDOWS_SOURCE) --distpath $(WINDOWS_OUTPUT)
	$(WINDOWS_OUTPUT)\wampus.exe

web:
	@echo "Building for web..."
	pip install flask
	python source/web/app.py

linux:
	@echo "Building for Linux..."
	@echo
	@echo "Installing python, pip, PyInstaller...\n"
	@apt install -y python3 python3-pip make
	@pip install --break-system-packages -r requirements.txt
	@echo "Done\n"
	@echo "Building Binary file..."
	@$(PYINSTALLER) $(LINUX_OPTIONS) $(LINUX_SOURCE) --distpath $(LINUX_OUTPUT)
	@echo "Done\n"
	@echo
	@echo "Built file located in $(LINUX_OUTPUT)"
	@echo

lpython3.12:
	@printf "Done\n"
	@echo
	@echo "Built file located in $(BSD_OUTPUT)"
	@echo

clean:
	@echo "Cleaning..."
	python $(CLEANING_FILE)

.PHONY: all windows linux web clean