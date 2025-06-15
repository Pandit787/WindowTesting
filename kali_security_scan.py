#!/usr/bin/env python3

import os
import subprocess
import sys
import time
from datetime import datetime

def check_root():
    """रूट एक्सेस की जांच करें"""
    return os.geteuid() == 0

def install_dependencies():
    """आवश्यक टूल्स इंस्टॉल करें"""
    print("\n[+] आवश्यक टूल्स जांच रहा हूँ...")
    tools = ['nmap', 'clamav', 'john', 'ufw', 'git']
    missing = []
    
    for tool in tools:
        try:
            subprocess.run(['which', tool], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            missing.append(tool)
    
    if missing:
        print(f"[-] निम्नलिखित टूल्स इंस्टॉल नहीं हैं: {', '.join(missing)}")
        choice = input("[?] क्या आप इन्हें इंस्टॉल करना चाहते हैं? (y/n): ").lower()
        if choice == 'y':
            try:
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y'] + missing, check=True)
                print("[+] टूल्स सफलतापूर्वक इंस्टॉल किए गए")
            except Exception as e:
                print(f"[-] इंस्टॉलेशन विफल: {str(e)}")
                sys.exit(1)
        else:
            print("[-] कुछ स्कैन्स काम नहीं करेंगे")
            time.sleep(2)

def run_nmap_scan(target_ip):
    """विस्तृत Nmap स्कैन चलाएं"""
    print(f"\n[+] {target_ip} पर Nmap स्कैन चल रहा है...")
    try:
        # व्यापक स्कैन जिसमें OS, सर्विस डिटेक्शन और वल्नरेबिलिटी स्कैन शामिल है
        commands = [
            ['sudo', 'nmap', '-T4', '-A', '-v', '-O', '-sV', '--script=vuln', target_ip],
            ['sudo', 'nmap', '--script', 'vulners', '-sV', target_ip],
            ['nmap', '-sV', '--script', 'banner', target_ip]
        ]
        
        for i, cmd in enumerate(commands, 1):
            print(f"\n[+] स्कैन {i}/{len(commands)} चल रहा है: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(result.stdout)
            
            with open(f'nmap_scan_{target_ip}_{i}.txt', 'w') as f:
                f.write(result.stdout)
                
    except Exception as e:
        print(f"[-] Nmap त्रुटि: {str(e)}")

def run_vulnerability_checks(target_ip):
    """अतिरिक्त सुरक्षा जांचें चलाएं"""
    print("\n[+] अतिरिक्त सुरक्षा जांचें चल रही हैं...")
    
    # Nikto स्कैन (अगर वेब सर्वर चल रहा है)
    try:
        print("\n[+] Nikto वेब स्कैन चल रहा है...")
        result = subprocess.run(
            ['nikto', '-h', target_ip],
            capture_output=True, text=True
        )
        print(result.stdout)
        with open(f'nikto_scan_{target_ip}.txt', 'w') as f:
            f.write(result.stdout)
    except FileNotFoundError:
        print("[-] Nikto इंस्टॉल नहीं है (sudo apt install nikto)")

    # WPScan (अगर WordPress चल रहा है)
    try:
        print("\n[+] WPScan चेक (अगर WordPress हो तो)...")
        result = subprocess.run(
            ['wpscan', '--url', f'http://{target_ip}', '--enumerate', 'vp'],
            capture_output=True, text=True
        )
        print(result.stdout)
        with open(f'wpscan_{target_ip}.txt', 'w') as f:
            f.write(result.stdout)
    except FileNotFoundError:
        print("[-] WPScan इंस्टॉल नहीं है")

def malware_scan():
    """ClamAV का उपयोग कर मैलवेयर स्कैन चलाएं"""
    print("\n[+] मैलवेयर स्कैन चल रहा है...")
    try:
        # ClamAV डेटाबेस अपडेट करें
        subprocess.run(['sudo', 'freshclam'], check=True)
        
        # क्विक स्कैन चलाएं
        result = subprocess.run(
            ['clamscan', '-r', '--bell', '-i', '/'],
            capture_output=True, text=True
        )
        print(result.stdout)
        with open('malware_scan.txt', 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"[-] मैलवेयर स्कैन विफल: {str(e)}")

def password_audit():
    """John the Ripper का उपयोग कर पासवर्ड ऑडिट"""
    print("\n[+] पासवर्ड ऑडिट सिमुलेशन चल रहा है...")
    try:
        # टेस्ट हैश फाइल बनाएं
        hashes = [
            "5f4dcc3b5aa765d61d8327deb882cf99",  # password
            "e10adc3949ba59abbe56e057f20f883e",  # 123456
            "25d55ad283aa400af464c76d713c07ad"   # 12345678
        ]
        
        with open('test_hashes.txt', 'w') as f:
            f.write("\n".join(hashes))
        
        print("John the Ripper चल रहा है...")
        result = subprocess.run(
            ['john', '--format=raw-md5', 'test_hashes.txt'],
            capture_output=True, text=True
        )
        print(result.stdout)
        
        # क्रैक किए गए पासवर्ड्स दिखाएं
        show_result = subprocess.run(
            ['john', '--show', 'test_hashes.txt'],
            capture_output=True, text=True
        )
        print(show_result.stdout)
        
        with open('password_audit.txt', 'w') as f:
            f.write(result.stdout + "\n" + show_result.stdout)
    except Exception as e:
        print(f"[-] पासवर्ड ऑडिट विफल: {str(e)}")

def system_hardening_check():
    """सिस्टम हार्डनिंग जांचें"""
    print("\n[+] सिस्टम हार्डनिंग जांचें चल रही हैं...")
    
    # फायरवॉल स्टेटस
    try:
        print("\n[+] UFW फायरवॉल स्टेटस:")
        result = subprocess.run(['sudo', 'ufw', 'status', 'verbose'], capture_output=True, text=True)
        print(result.stdout)
        
        with open('firewall_status.txt', 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"[-] फायरवॉल जांच विफल: {str(e)}")
    
    # अपडेटेबल पैकेज्स
    try:
        print("\n[+] उपलब्ध अपडेट्स:")
        result = subprocess.run(['apt', 'list', '--upgradable'], capture_output=True, text=True)
        print(result.stdout)
        
        with open('system_updates.txt', 'w') as f:
            f.write(result.stdout)
    except Exception as e:
        print(f"[-] अपडेट जांच विफल: {str(e)}")

def generate_report(target_ip):
    """संपूर्ण रिपोर्ट जनरेट करें"""
    print("\n[+] अंतिम रिपोर्ट जनरेट कर रहा हूँ...")
    report = f"""
    काली लिनक्स सुरक्षा स्कैन रिपोर्ट
    ================================
    तिथि: {datetime.now()}
    लक्ष्य IP: {target_ip}
    
    किए गए स्कैन:
    - Nmap पोर्ट और वल्नरेबिलिटी स्कैन
    - वेब एप्लिकेशन स्कैन (Nikto/WPScan)
    - मैलवेयर स्कैन (ClamAV)
    - पासवर्ड स्ट्रेंथ ऑडिट (John the Ripper)
    - सिस्टम हार्डनिंग जांच
    
    उत्पन्न फाइलें:
    - nmap_scan_*.txt - Nmap स्कैन परिणाम
    - nikto_scan_{target_ip}.txt - Nikto वेब स्कैन
    - wpscan_{target_ip}.txt - WPScan परिणाम
    - malware_scan.txt - मैलवेयर स्कैन रिपोर्ट
    - password_audit.txt - पासवर्ड ऑडिट रिपोर्ट
    - firewall_status.txt - फायरवॉल स्थिति
    - system_updates.txt - उपलब्ध सिस्टम अपडेट्स
    
    सिफारिशें:
    1. सभी उपलब्ध सिस्टम अपडेट्स इंस्टॉल करें
    2. कमजोर पासवर्ड बदलें
    3. अनावश्यक खुले पोर्ट्स बंद करें
    4. फायरवॉल कॉन्फिगरेशन की समीक्षा करें
    5. किसी भी मैलवेयर पाये जाने पर जांच करें
    """
    
    print(report)
    with open('security_report.txt', 'w') as f:
        f.write(report)

def main():
    print("""
    ██╗  ██╗ █████╗ ██╗     ██╗    ███████╗ ██████╗ ██╗   ██╗███████╗██████╗ 
    ██║ ██╔╝██╔══██╗██║     ██║    ██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗
    █████╔╝ ███████║██║     ██║    ███████╗██║   ██║██║   ██║█████╗  ██████╔╝
    ██╔═██╗ ██╔══██║██║     ██║    ╚════██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
    ██║  ██╗██║  ██║███████╗██║    ███████║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝    ╚══════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
    """)
    
    if not check_root():
        print("[-] चेतावनी: कुछ स्कैन्स के लिए रूट एक्सेस आवश्यक है")
    
    install_dependencies()
    
    target_ip = input("\n[?] लक्ष्य IP एड्रेस दर्ज करें (या 'localhost'): ").strip()
    if target_ip.lower() == 'localhost':
        target_ip = '127.0.0.1'
    
    print(f"\n[+] {target_ip} के लिए सुरक्षा स्कैन शुरू कर रहा हूँ...")
    
    # मुख्य स्कैन फंक्शन्स
    run_nmap_scan(target_ip)
    run_vulnerability_checks(target_ip)
    malware_scan()
    password_audit()
    system_hardening_check()
    
    # अंतिम रिपोर्ट
    generate_report(target_ip)
    
    print("\n[+] स्कैन पूर्ण! सभी परिणाम टेक्स्ट फाइल्स में सहेजे गए हैं")

if __name__ == "__main__":
    main()
