import os
import json
"""
main_settings = {}

folders_scan = {}
"""
folder_structure = {
    'Foto\'s': None,
    'Plannen': None,
    'Stabiliteit': [
        'Algemene documenten',
        'Berekeningen',
        'Berekeningen Scia',
        'Mails',
        'Meetstaat & borderel',
        'Plannen pdf',
        'Sondeerverslag',
        'Stabiliteitsplannen'
        ],
    'Ventilatieverslaggever': None,
    'vVGP + EPB': [
        'EPB',
        'VGP'],
    'Werfverslagen': None
    }

class Settings():
    # dossier = dict in dict -- dossier[nr][name or path]
    # load main settings

    """
    #####################################################################
                            loading/saving functions
    #####################################################################
    """
    def loader(self):
        """
        load setting / create default setting when none exists
            - main settings
            - folders
        """
        print("loading settings")
        # DEFAULT settings contents
        self.main_settings = {"directory": "none selected"}
        self.folder_scan = {}
        # load settings
        settings = self.loadjson("settings.txt", self.main_settings)        # settings.py
        folders = self.loadjson("folders.txt", self.folder_scan)
        return settings, folders    #returns a tuple

    def loadjson(self, filename, setting):
        """
        load filename if exists,
            else create filename and populate with default
        """
        print("creating\n{} \npopulating with\n{}".format(filename, setting))
        try:
            with open(filename,"r") as f:
                setting = json.load(f)
        except:
            print("creating", setting)
            with open(filename,"w") as f:
                json.dump(setting, f)
        return setting

    """---------------------------------------------------
    save settings function              change (filename, setting) input order
    """
    def save_set(self, filename, setting):
        with open(filename,"w") as f:
            json.dump(setting, f, indent = 4) # changed order (settings, f) from (f, settings)
        print(setting)

    """---------------------------------------------------
    """
    def load_set(self, name):
        """?    needs to save setting + does not load, but gets specific setting, change name?"""
        print("loads specific setting(?) + checks for existing setting (?)")
        with open("settings.txt", "r") as f:
            self.settings = json.load(f)
        if name in self.settings:
            print("found setting")
            print(self.settings[name])
            return self.settings[name]
        else:
            print("nothing found")
            pass

    #loads dossier settings
    """ADD check for missing folders here?
    """
    def load_dossier(self, dossier):
        print("loads dossier(?)")
        with open("folders.txt", "r") as f:
            self.loading = json.load(f)
            print(self.loading[dossier])
            return self.loading[dossier]


    def read_folders(self, scanpath):
        """
        returns dictionary with name,path for each folder(/dossier)
        from foldernames structure 'dossier - name'
        """
        print("reading folders: dossier/name/path")
        self.dossier = {}
        dirs = os.listdir(scanpath)
        for folder in dirs:
            path = os.path.join(scanpath, folder)
            if ' - ' in folder and os.path.isdir(path):
                print('processing\n', folder)
                prefix, suffix = folder.split(' - ', 1)
                self.dossier[prefix] = {"name": suffix, "path": path}
        print("returning\n", self.dossier)
        return self.dossier


        """
        ?       one of the other = other       ?
        """
        """
        #check if dirs exist for ALL SAVED dossiers
        def check_folders(self, folder_scan):
        """
        #ONLY DO THIS FOR INPUT DOSSIER? ? ? ?
        """
        for key in folder_scan:
            print(key)
            print(folder_scan[key])
            print(folder_scan[key]['path'])
            for maps in folder_structure:
                if folder_structure[maps] == None:
                    print("none for {}".format(maps))
                    scanpath = folder_scan[key]['path'] + "//" + maps
                    print(scanpath)
                    self.create_dirs(scanpath)
                else:
                    print("map for {}".format(maps))
                    print(folder_structure[maps])

                    #fix item is list iterate trough list?
                    for item in folder_structure[maps]:
                        print(item)
                        scanpath = folder_scan[key]['path'] + "//" + maps + "//" + item
                        print(scanpath)
                        self.create_dirs(scanpath)
        """
    #check if dirs exist for SPECIFIC dossiers
    def dossier_dir(self, folder_scan):
        """
        create dictionary structure for specific dossier folder
        so we can check against existing structure
        """
        #global folder_structure
        for folder, subfolder in folder_structure.items():
            if subfolder == None:
                scanpath = folder_scan['path'] + "//" + maps
            else:
                for subfolder in folder_structure[folder]:
                    scanpath = folder_scan['path'] + "//" + maps + "//" + item
            self.create_dirs(scanpath)



    # create dirs if they don't exist
    def create_dirs(self, scanpath):
        """
        ADD ??
        if not os.path.exists(directory):
        os.makedirs(directory)
        """

        """
        BETTER ADD??
        import errno

        def make_sure_path_exists(path):
            try:
                os.makedirs(path)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

                    we try to create the directories, but if they
                    already exist we ignore the error.
                    On the other hand, any other error gets reported.
                    For example, if you create dir 'a' beforehand and
                    remove all permissions from it,you will get an
                    OSError raised with errno.EACCES (Permission denied,
                    error 13).
        """
        print("create nonexisting dirs")
        try:
            print("only scans paths(?)")

            os.makedirs(scanpath)
        except OSError:
            if not os.path.isdir(scanpath):
                print("if not existing (?) ADD STUFF CHECK Settings.py")
                raise

    def structure(self):
        return folder_structure
