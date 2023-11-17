
from loguru import logger


class MdFile:
    def __init__(self, md_path):
        self.md_path = md_path
        with open(self.md_path, 'r') as f:
            self.content = f.read()

    def replace(self, recognizer, replace_func):
        items = recognizer.findall(self.content)
        logger.info(f"{recognizer.name} found {len(items)} items:")
        for item in items:
            logger.info(f"    {item}")
        replace_dict = {}
        for item in items:
            replace_dict[item] = replace_func(item)
        self.content = recognizer.multiple_replace(self.content, **replace_dict)

    def save(self):
        with open(self.md_path, 'w') as f:
            f.write(self.content)
