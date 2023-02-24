pip install --upgrade pip
pip install pyinstaller
pip install customtkinter
pip install Pillow
pip install pycopy-webbrowser
pip install tkfilebrowser
pip install opencv-python
pip install pytest-shutil

pyinstaller --onefile --windowed --icon "icon.ico" --add-data "C:/Users/darkd/AppData/Local/Programs/Python/Python310/Lib/site-packages/customtkinter;customtkinter/" "Cartoonizer.py" -w -F

rmdir /s /q build

:cmd
pause null