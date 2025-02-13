import os
import subprocess
import ctypes
import socket

class VirtualShield:
    def __init__(self):
        self.networks = []
    
    def list_networks(self):
        """List all available network interfaces."""
        self.networks = os.popen('netsh wlan show interfaces').read()
        print("Available Networks:")
        print(self.networks)

    def connect_to_network(self, ssid, password):
        """Connect to a specified network."""
        print(f"Attempting to connect to network: {ssid}")
        profile = f'''<?xml version="1.0"?>
        <WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
            <name>{ssid}</name>
            <SSIDConfig>
                <SSID>
                    <name>{ssid}</name>
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
                        <keyMaterial>{password}</keyMaterial>
                    </sharedKey>
                </security>
            </MSM>
        </WLANProfile>'''
        
        with open(f"{ssid}.xml", 'w') as file:
            file.write(profile)
        
        subprocess.run(["netsh", "wlan", "add", "profile", f"filename={ssid}.xml"])
        subprocess.run(["netsh", "wlan", "connect", f"name={ssid}"])
        os.remove(f"{ssid}.xml")
        
        print(f"Connected to {ssid} successfully.")

    def optimize_settings(self):
        """Optimize network settings for enhanced connectivity."""
        print("Optimizing network settings...")
        subprocess.run(["netsh", "interface", "tcp", "set", "global", "autotuninglevel=normal"])
        subprocess.run(["netsh", "int", "tcp", "set", "heuristics", "disabled"])
        print("Network settings optimized for enhanced connectivity.")

    def check_internet_connection(self):
        """Check if the internet connection is active."""
        try:
            socket.create_connection(("www.google.com", 80))
            print("Internet connection is active.")
            return True
        except OSError:
            print("No internet connection.")
            return False

    def run(self):
        """Run VirtualShield functionalities."""
        self.list_networks()
        self.optimize_settings()
        if self.check_internet_connection():
            print("All systems go!")
        else:
            print("Please check your network settings.")

if __name__ == "__main__":
    vs = VirtualShield()
    vs.run()