from GenUECompileCommand import main as gen_compile_commands

import os,shutil

def copy_clang_config():
    tools_dir = os.path.dirname(__file__);
    shutil.copy(
        os.path.join(tools_dir, '.clangd'),
        os.path.join(os.getcwd(), '.clangd')
    );
    print('--- copy clangd config finished ---')

if __name__ == '__main__':
    gen_compile_commands()
    copy_clang_config()

