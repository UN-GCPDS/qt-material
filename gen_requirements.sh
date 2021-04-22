rm requirements.txt
pipreqs --savepath requirements.txt --force qt_material
sed -i '/PyQt5/d' requirements.txt
sed -i '/PyQt6/d' requirements.txt
sed -i '/PySide2/d' requirements.txt
sed -i '/PySide6/d' requirements.txt
sed -i 's/==.*//' requirements.txt
python -c "[print(f'\'{line[:-1]}\',') for line in open('requirements.txt').readlines()]"
