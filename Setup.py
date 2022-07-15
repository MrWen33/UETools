from GenUECompileCommand import main as gen_compile_commands

import os,subprocess

def copy_clang_config():
    tools_dir = os.path.dirname(__file__);
    subprocess.run(['copy', 
        os.path.join(tools_dir, '.clangd'),
        os.path.join(os.getcwd(), '.clangd')
        ], shell=True)

if __name__ == '__main__':
    gen_compile_commands()
    copy_clang_config()

