pipreqs --savepath requirements.tmp --force qt_material
rm requirements.txt

sed '/PyQt5/d' requirements.tmp >> requirements.txt
mv requirements.txt requirements.tmp

sed '/PyQt6/d' requirements.tmp >> requirements.txt
mv requirements.txt requirements.tmp

sed '/PySide2/d' requirements.tmp >> requirements.txt
mv requirements.txt requirements.tmp

sed '/PySide6/d' requirements.tmp >> requirements.txt

rm requirements.tmp
cat requirements.txt