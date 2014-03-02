import sys
import os
from subprocess import Popen, PIPE, call
from shutil import rmtree


def get_steam_directory():
    import winreg as registry

    key = registry.CreateKey(registry.HKEY_CURRENT_USER, "Software\\Valve\\Steam")
    return registry.QueryValueEx(key, "SteamPath")[0]


def get_dota_directory():
    return get_steam_directory() + '/steamapps/common/dota 2 beta/dota'


def extract_skin(dota_directory, skin_name):
    data_path = 'root\\resource\\flash3\\images\\hud_skins\\' + skin_name
    out_path = dota_directory + "/resource/flash3/images/hud_skins/"
    skin_path = out_path + skin_name + '/'
    if not os.path.exists(out_path):  # if the output directory doesnt exist, create it
        os.makedirs(out_path)
        print("created %s" % out_path)

    try:
        rmtree(out_path + 'default/')  #otherwise, clear the default directory
        print('deleted %s ' % (out_path + 'default/'))
    except:
        pass  # no need to worry about it if the directory doesn't exist
    try:
        rmtree(skin_path)  #and the temp skin directory
        print('deleted %s ' % (skin_path))
    except:
        pass
    cmd = 'HLExtract.exe -v -p "{0}" -d "{1}" -e "{2}"'.format(dota_directory + '/pak01_dir.vpk', out_path, data_path)
    print(cmd)
    call(cmd)
    if not os.path.exists(skin_path):
        raise Exception("%s doesn't exist, but it should! Did extracting go wrong?" % (skin_path))
    else:
        print("Success.")
    print("Setting new HUD as default...")
    os.rename(skin_path, out_path + 'default/')


def get_skin_name(filename):
    #I HATE REGEX I DON'T NEED IT
    prefix = 'root\\resource\\flash3\\images\\hud_skins\\'
    if not filename.startswith(prefix):  #if not a hud skin
        return None  #skip it
    filename = filename[len(prefix):]
    if '\\' in filename:  #only want the name of the skin root
        return None
    return str(filename).replace('\r', '')


def list_skins(dota_directory):
    cmd = 'HLExtract.exe -v -p "{0}" -l'.format(dota_directory + '/pak01_dir.vpk')
    pipe = Popen(cmd, stdout=PIPE)
    text = pipe.communicate()[0].decode()
    lines = text.split('\n')
    skins = [get_skin_name(x) for x in lines if (get_skin_name(x) is not None and get_skin_name(x) != "default")]
    if os.path.exists(dota_directory + "/resource/flash3/images/hud_skins/default/"):
        skins.append("[Restore default HUD]")
    return skins


def uninstall(dota_directory):
    out_path = dota_directory + "/resource/flash3/images/hud_skins/default/"
    if os.path.exists(out_path):
        rmtree(out_path)
        print('Deleted ' + out_path)
    else:
        print('Nothing to delete.')


def main():
    #get dota 2 directory & verify
    if len(sys.argv) > 1:
        dota_directory = sys.argv[1]
        if not os.path.isdir(dota_directory):
            print("%s doesn't exist! Please pass the correct one as a parameter." % dota_directory)
            return
    else:
        dota_directory = get_steam_directory() + '/steamapps/common/dota 2 beta/dota'
        if not os.path.isdir(dota_directory):
            print(
                "Dota 2 directory should be %s but it doesn't exist! Please pass the correct one as a parameter." % dota_directory)
            return

    print("Looking for HUDs in Dota 2's data...")
    skins = list_skins(dota_directory)
    print("Available HUDs:")
    for idx, val in enumerate(skins):
        print("%s. %s" % (idx, val))
    user_input = ''
    while not (user_input.isdigit() and int(user_input) < len(skins)):
        user_input = input("Enter the number of the desired HUD: ")
    skin = skins[int(user_input)]
    if skin == "[Restore Original HUD]":
        uninstall(dota_directory)
    else:
        print("Begin extracting " + skin)
        extract_skin(dota_directory, skin)
    print("Done!")
    input("Press enter to exit")


if __name__ == '__main__':
    main()