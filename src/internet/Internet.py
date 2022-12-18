import os
from urllib import request

PATH_SAVED = "src/internet/profiles"
def create_new_connection(name, ssid, password):
  config = """<?xml version=\"1.0\"?>
    <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+ssid+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+password+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
    </WLANProfile>"""
  filename = PATH_SAVED + "/" + name
  command = "netsh wlan add profile filename=\""+filename+".xml\""+" interface=Wi-Fi"
  with open(filename+".xml", 'w') as file:
    file.write(config)
  os.system(command)

def connect(name, ssid):
  command = "netsh wlan connect name=\""+name+"\" ssid=\""+ssid+"\" interface=Wi-Fi"
  os.system(command)

def available():
  command = "netsh wlan show networks interface=Wi-Fi"
  os.system(command)

class Internet:
  def __init__(self, name, ssid, password):
    self.name = name
    self.ssid = ssid
    self.password = password

  def create_new_connection(self):
    create_new_connection(self.name, self.ssid, self.password)
  
  def connect(self):
    connect(self.name, self.ssid)
  
  def available(self):
    available()

  def run(self):
    file_name = PATH_SAVED + "/" + self.name + ".xml"
    if os.path.exists(file_name) == False:
      self.create_new_connection()
    self.connect()
    
  @staticmethod
  def internet_connection():
    try:
      request.urlopen("http://google.com")
      return True
    except Exception as __e:
      return False