import os
import shutil
from pathlib import Path


HOME = Path.home()
RESOURCES_PATH = os.path.join(HOME, '.qt_material')
SOURCE = os.path.join(os.path.dirname(__file__), 'source')


if not os.path.exists(RESOURCES_PATH):
    os.mkdir(RESOURCES_PATH)


# # primary_icons = os.listdir(SOURCE)

# # contex = [
    # # ('disabled', '#ff0000'),
    # # ('primary', '#0000ff'),
# # ]


# # ----------------------------------------------------------------------
# def replace_color(content, replace, color='#0000ff'):
    # """"""
    # colors = [color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
    # for c in colors:
        # content = content.replace(c, replace)

    # replace = '#ffffff00'
    # color = '#000000'
    # colors = [color] + [''.join(list(color)[:i] + ['\\\n'] + list(color)[i:]) for i in range(1, 7)]
    # for c in colors:
        # content = content.replace(c, replace)

    # return content


# # # ----------------------------------------------------------------------
# # def create_qrc(qrc):
    # # """"""
    # # with open(QRC_FILE, 'w') as file:

        # # file.write('<RCC>\n')
        # # for key in qrc:
            # # file.write(f'  <qresource prefix="{key}">\n')
            # # for icon in qrc[key]:
                # # # icon = icon.replace(f'{key}/', '')
                # # file.write(f'    <file>{icon}</file>\n')
            # # file.write(f'  </qresource>\n')
        # # file.write('</RCC>\n')


# # for folder, _ in contex:
    # # shutil.rmtree(folder, ignore_errors=True)
    # # os.mkdir(folder)
    # # # qrc[folder] = []

# for icon in primary_icons:
    # if not icon.endswith('.svg'):
        # continue

    # with open(os.path.join(SOURCE, icon), 'r') as file_input:
        # original = file_input.read()

        # for folder, color in contex:
            # new_content = replace_color(original, color)

            # file_to_write = os.path.join(folder, icon)

            # # qrc[folder] += [file_to_write]
            # qrc['icon'] += [file_to_write]

            # with open(file_to_write, 'w') as file_output:
                # file_output.write(new_content)
                # # print(f"created {file_to_write}")


########################################################################
class ResourseGenerator:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, primary, disabled, parent='theme'):
        """Constructor"""

        self.contex = [
            (os.path.join(RESOURCES_PATH, parent, 'disabled'), disabled),
            (os.path.join(RESOURCES_PATH, parent, 'primary'), primary),
        ]

        for folder, _ in self.contex:
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder, exist_ok=True)

        self.index = os.path.join(RESOURCES_PATH, parent)

    # ----------------------------------------------------------------------
    def generate(self):
        """"""
        for icon in os.listdir(SOURCE):
            if not icon.endswith('.svg'):
                continue

            with open(os.path.join(SOURCE, icon), 'r') as file_input:
                original = file_input.read()

                for folder, color in self.contex:
                    new_content = self.replace_color(original, color)

                    file_to_write = os.path.join(folder, icon)

                    # qrc[folder] += [file_to_write]
                    # qrc['icon'] += [file_to_write]

                    with open(file_to_write, 'w') as file_output:
                        file_output.write(new_content)
                        # print(f"created {file_to_write}")

    # ----------------------------------------------------------------------
    def replace_color(self, content, replace, color='#0000ff'):
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
