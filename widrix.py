import subprocess
import sys

def run_command(command, description):
    print(f"[+] {description}... \n$ {command}")
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error occurred: {e}")
        sys.exit(1)

def check_internet():
    print("[+] Checking internet connection...")
    try:
        subprocess.run("ping -c 1 8.8.8.8", check=True, shell=True, stdout=subprocess.DEVNULL)
        print("[+] Internet connection is available!\n")
    except subprocess.CalledProcessError:
        print("[-] No internet connection! Please check your network.")
        sys.exit(1)

def check_wifi_adapter():
    print("[+] Checking USB Wi-Fi adapter...")
    result = subprocess.run("lsusb", shell=True, capture_output=True, text=True)
    if "8821" in result.stdout:
        print("[+] RTL8821AU adapter detected!\n")
    else:
        print("[-] RTL8821AU adapter not found!\n")
        sys.exit(1)

def confirm():
    answer = input("Do you want to continue? (Y/n): ").strip().lower()
    if answer not in ["y", "yes"]:
        print("[-] Operation canceled.")
        sys.exit(0)

def success_message():
    nick = "xiesorie"
    print(f"\n[✔] All tasks completed successfully! - By {nick}")


def main():
    print("\n*** Widrix - RTL8821AU Driver Installer ***\n")
    check_internet()
    check_wifi_adapter()
    confirm()
    
    run_command("sudo apt update && sudo apt upgrade -y", "Updating system")
    run_command("sudo apt install -y build-essential dkms git iw bc libelf-dev linux-headers-$(uname -r) rfkill", "Installing dependencies")
    run_command("git clone https://github.com/morrownr/8821au-20210708.git", "Downloading RTL8821AU driver")
    run_command("cd 8821au-20210708 && sudo ./install-driver.sh", "Installing driver")
    run_command("sudo dkms status", "Checking driver status")
    
    print("\n[+] Installation complete! A system reboot is recommended.")
    confirm()
    run_command("sudo reboot", "Rebooting system")
    
    success_message()


if __name__ == "__main__":
    main()
