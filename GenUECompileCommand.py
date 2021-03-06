import os, winreg, json;
import subprocess
import shutil

def get_uproject_file_abs_path(dir_path):
    results = list(filter(lambda f: f.endswith('.uproject'), os.listdir(dir_path)))
    if len(results) < 0:
        return None;
    return os.path.join(os.path.abspath(dir_path),results[0]);


def find_ue_path_winreg(key):
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as reg:
        arg = r'SOFTWARE\Epic Games\Unreal Engine\Builds';
        reg_key = winreg.OpenKey(reg, arg)
        val = winreg.QueryValueEx(reg_key, key)[0]
        return val
    

def get_engine_path_from_uproject(uproject_path):
    with open(uproject_path, 'r') as f:
        json_content = json.load(f)
    key = json_content['EngineAssociation']
    return find_ue_path_winreg(key)

def gen_compile_commands(engine_path: str, uproject_path: str, output_dir='.'):
    ubt_rel_path = r'Engine\Binaries\DotNET\UnrealBuildTool\UnrealBuildTool.exe' # ue5 ubt path
    if not os.path.isfile(os.path.join(engine_path,ubt_rel_path)):
        ubt_rel_path = r'Engine\Binaries\DotNET\UnrealBuildTool.exe' # ue4 ubt path

    # gen compile commands file
    ubt_abs_path = os.path.join(engine_path, ubt_rel_path)
    uproj_name = os.path.splitext(os.path.basename(uproject_path))[0]
    subprocess.run([
        ubt_abs_path, 
        f'{uproj_name}Editor',
        'Win64',
        'Development',
        '-SkipBuild',
        f'-project={uproject_path}',
        '-game',
        '-engine',
        '-mode=GenerateClangDatabase'])
    print(' --- json file generated --- ')

    # move compile commands file
    file_name = 'compile_commands.json'
    shutil.move(
        os.path.join(engine_path, file_name),
        os.path.join(os.path.abspath(output_dir), file_name)
            )
    print(' --- json file moved --- ')

def main():
    print('---- generating compile commands ----')
    uproject_path = get_uproject_file_abs_path('.');
    print(f'uproject_path: {uproject_path}')
    if uproject_path is None:
        print('ERROR: uproject not found in current dir. Abort')
        return

    engine_path = get_engine_path_from_uproject(uproject_path)
    print(f'engine_path: {engine_path}')
    gen_compile_commands(engine_path, uproject_path)
    print('---- done ----')

if __name__ == '__main__':
    main()

