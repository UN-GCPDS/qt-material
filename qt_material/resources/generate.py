import os
import shutil
from pathlib import Path

HOME = Path.home()
RESOURCES_PATH = os.path.join(HOME, '.qt_material')


########################################################################
class ResourseGenerator:
    """"""

    # ----------------------------------------------------------------------
    def __init__(
        self,
        primary,
        secondary,
        disabled,
        source,
        parent='theme',
    ):
        """Constructor"""

        if parent.startswith('/'):
            self.index = parent
        if parent.startswith('.'):
            self.index = parent[1:]
        else:
            self.index = os.path.join(RESOURCES_PATH, parent)

        active = '#707070'

        self.contex = [
            (os.path.join(self.index, 'disabled'), disabled),
            (os.path.join(self.index, 'primary'), primary),
            (os.path.join(self.index, 'active'), active),
        ]

        self.source = source
        self.secondary = secondary

        for folder, _ in self.contex:
            shutil.rmtree(folder, ignore_errors=True)
            os.makedirs(folder, exist_ok=True)

    # ----------------------------------------------------------------------

    def generate(self):
        """"""
        for icon in os.listdir(self.source):
            if not icon.endswith('.svg'):
                continue

            with open(os.path.join(self.source, icon), 'r') as file_input:
                content_original = file_input.read()

                for folder, color in self.contex:
                    new_content = self.replace_color(content_original, color)
                    new_content = self.replace_color(
                        new_content, self.secondary, '#ff0000'
                    )

                    file_to_write = os.path.join(folder, icon)
                    with open(file_to_write, 'w') as file_output:
                        file_output.write(new_content)

    # ----------------------------------------------------------------------
    def replace_color(self, content, replace, color='#0000ff'):
        """"""
        colors = [color] + [
            ''.join(list(color)[:i] + ['\\\n'] + list(color)[i:])
            for i in range(1, 7)
        ]
        for c in colors:
            content = content.replace(c, replace)

        replace = '#ffffff00'
        color = '#000000'
        colors = [color] + [
            ''.join(list(color)[:i] + ['\\\n'] + list(color)[i:])
            for i in range(1, 7)
        ]
        for c in colors:
            content = content.replace(c, replace)

        return content
