import os
import shutil


SOURCE = 'source'
QRC_FILE = 'resource.qrc'


primary_icons = os.listdir(SOURCE)

contex = [
    ('disabled', '#ff0000'),
    ('primary', '#0000ff'),
]

qrc = {
    'icon': [],
}


# ----------------------------------------------------------------------
def replace_color(content, replace, color='#0000ff'):
    """"""
    colors = [color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
    for c in colors:
        content = content.replace(c, replace)

    replace = '#ffffff00'
    color = '#000000'
    colors = [color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
    for c in colors:
        content = content.replace(c, replace)

    return content


# ----------------------------------------------------------------------
def create_qrc(qrc):
    """"""
    with open(QRC_FILE, 'w') as file:

        file.write('<RCC>\n')
        for key in qrc:
            file.write(f'  <qresource prefix="{key}">\n')
            for icon in qrc[key]:
                # icon = icon.replace(f'{key}/', '')
                file.write(f'    <file>{icon}</file>\n')
            file.write(f'  </qresource>\n')
        file.write('</RCC>\n')


for folder, _ in contex:
    shutil.rmtree(folder, ignore_errors=True)
    os.mkdir(folder)
    # qrc[folder] = []

for icon in primary_icons:
    if not icon.endswith('.svg'):
        continue

    with open(os.path.join(SOURCE, icon), 'r') as file_input:
        original = file_input.read()

        for folder, color in contex:
            new_content = replace_color(original, color)

            file_to_write = os.path.join(folder, icon)

            # qrc[folder] += [file_to_write]
            qrc['icon'] += [file_to_write]

            with open(file_to_write, 'w') as file_output:
                file_output.write(new_content)
                # print(f"created {file_to_write}")


create_qrc(qrc)


for qrc_file in [QRC_FILE, 'logos.qrc']:

    RCC = 'pyside2-rcc --no-compress --verbose'
    command_pyside = f"{RCC} {qrc_file}  -o {qrc_file.replace('.qrc', '_pyside2_rc.py')}"
    os.system(command_pyside)

    RCC = 'pyside6-rcc --no-compress --verbose'
    command_pyside = f"{RCC} {qrc_file}  -o {qrc_file.replace('.qrc', '_pyside6_rc.py')}"
    os.system(command_pyside)

    RCC = 'pyrcc5 -no-compress'
    command_qt = f"{RCC} {qrc_file}  -o {qrc_file.replace('.qrc', '_pyqt5_rc.py')}"
    os.system(command_qt)
