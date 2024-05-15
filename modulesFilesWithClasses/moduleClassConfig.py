import configparser
import os
import time


class Config():
    def __init__(self):
        self.ConfigFile = 'config.cfg'
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.config.add_section("Settings")
        #config.set("Settings", "bot_token", "token")
        #config.set("Settings", "admin_id_own", "0:1")  # [1, 2]
        #config.set("Settings", "admin_id_manager", "0:1")
        #config.set("Settings", "bot_login", "0")
        #config.set("Settings", "ref_percent", "0")
        #config.set("Settings", "qiwi_number", "0")
        #config.set("Settings", "qiwi_token", "0")
        #config.set("Settings", "api_smshub", "0")
        with open(self.ConfigFile, "w") as config_file:
            self.config.write(config_file)

    def check_config_file(self):
        if not os.path.exists(self.ConfigFile):
            self.create_config()
            print('Config created')
            time.sleep(3)
            exit(0)

    def config(self, what):
        self.config.read(self.ConfigFile)
        value = self.config.get("Settings", what)
        return value

    def edit_config(self, setting, value):
        self.config.read(self.ConfigFile)
        self.config.set("Settings", setting, value)
        with open(self.ConfigFile, "w") as config_file:
            self.config.write(config_file)


#check_config_file()
