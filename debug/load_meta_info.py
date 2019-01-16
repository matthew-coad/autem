if __name__ == '__main__':
    import context

import genetic
from config import REPOSITORY_PATH

meta_manager = genetic.MetaManager(REPOSITORY_PATH)
meta_info = meta_manager.get_meta_info()

import code
code.InteractiveConsole(locals=globals()).interact()
