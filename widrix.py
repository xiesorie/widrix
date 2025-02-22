import subprocess
import sys

def run_command(command, description):
    """Komutları çalıştıran yardımcı fonksiyon"""
    print(f"[+] {description}... \n$ {command}")
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Hata oluştu: {e}")
        sys.exit(1)

def check_internet():
    """İnternet bağlantısını kontrol eder"""
    print("[+] İnternet bağlantısı kontrol ediliyor...")
    try:
        subprocess.run("ping -c 1 8.8.8.8", check=True, shell=True, stdout=subprocess.DEVNULL)
        print("[+] İnternet bağlantısı mevcut!\n")
    except subprocess.CalledProcessError:
        print("[-] İnternet bağlantısı bulunamadı! Lütfen kontrol edin.")
        sys.exit(1)

def check_wifi_adapter():
    """Wi-Fi adaptörünün RTL8821AU olup olmadığını kontrol eder"""
    print("[+] USB Wi-Fi adaptörü kontrol ediliyor...")
    result = subprocess.run("lsusb", shell=True, capture_output=True, text=True)
    if "8821" in result.stdout:
        print("[+] RTL8821AU adaptörü bulundu!\n")
    else:
        print("[-] RTL8821AU adaptörü bulunamadı!\n")
        sys.exit(1)

def confirm():
    """Kullanıcıdan onay alır"""
    answer = input("Devam etmek istiyor musunuz? (E/h): ").strip().lower()
    if answer not in ["e", "evet", "yes", "y"]:
        print("[-] İşlem iptal edildi.")
        sys.exit(0)

def main():
    print("\n*** Widrix - RTL8821AU Driver Installer ***\n")
    check_internet()
    check_wifi_adapter()
    confirm()
    
    run_command("sudo apt update && sudo apt upgrade -y", "Sistem güncelleniyor")
    run_command("sudo apt install -y build-essential dkms git iw bc libelf-dev linux-headers-$(uname -r) rfkill", "Gerekli bağımlılıklar yükleniyor")
    run_command("git clone https://github.com/morrownr/8821au-20210708.git", "RTL8821AU sürücüsü indiriliyor")
    run_command("cd 8821au-20210708 && sudo ./install-driver.sh", "Sürücü kuruluyor")
    run_command("sudo dkms status", "Sürücü durumu kontrol ediliyor")
    
    print("\n[+] Kurulum tamamlandı! Sistemi yeniden başlatmanız önerilir.")
    confirm()
    run_command("sudo reboot", "Sistem yeniden başlatılıyor")

if __name__ == "__main__":
    main()
