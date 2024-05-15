import configparser
import os
import time


class Config():
    def __init__(self):
        self.ConfigFile = 'config.cfg'
        self.config = configparser.ConfigParser()

    def create_config(self):
        self.config.add_section("Settings")
        self.config.set("Settings", "ServerNameRemote", "data-server-1.movistar.vrn.skylink.local")
        self.config.set("Settings", "ServerNameOriginal", "localhost\mssqlserver15")
        self.config.set("Settings", "ServerHost", "localhost\mssqlserver15")
        self.config.set("Settings", "ServerNameFlights", "_")
        self.config.set("Settings", "ServerName", "_")
        self.config.set("Settings", "ServerNameDeveloper", "_")
        with open(self.ConfigFile, "w") as config_file:
            self.config.write(config_file)

    def check_config_file(self):
        if not os.path.exists(self.ConfigFile):
            self.create_config()
            print('Config created')
            time.sleep(3)
            exit(0)

    def read_config_Settings(self, value):
        self.config.read(self.ConfigFile)
        value = self.config.get("Settings", value)
        return value

    def edit_config(self, setting, value):
        self.config.read(self.ConfigFile)
        self.config.set("Settings", setting, value)
        with open(self.ConfigFile, "w") as config_file:
            self.config.write(config_file)


#check_config_file()
