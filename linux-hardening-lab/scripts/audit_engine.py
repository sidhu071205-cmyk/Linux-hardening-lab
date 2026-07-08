import paramiko
import nmap
import sys
TARGET_IP = "192.168.60.128"
SSH_PORT = 2222
USERNAME = "sysadmin"
KEY_PATH = "/home/kali/.ssh/id_ed25519"
SUDO_PASS = "YOUR_PASSWORD_HERE" # Required for paramiko to execute sudo
print(f"[*] Starting Custom Security Audit on {TARGET_IP}...\n")
# Prompt the user for Auto-Remediation
auto_fix = input("Do you want to automatically remediate vulnerabilities found? (y/n): ").strip().lower()
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(TARGET_IP, port=SSH_PORT, username=USERNAME, key_filename=KEY_PATH)
    def run_sudo_cmd(command):
        """Helper function to execute sudo commands without hanging."""
        stdin, stdout, stderr = client.exec_command(f"sudo -S {command}")
        stdin.write(f"{SUDO_PASS}\n")
        stdin.flush()
        return stdout.read().decode('utf-8').strip(), stderr.read().decode('utf-8').strip()
    # --- AUDIT 1: Rogue User ---
    print("\n[*] Checking rogueuser account lifecycle...")
    out, err = run_sudo_cmd("chage -l rogueuser | grep 'Maximum number'")
    print(f"    Current Status: {out}")
    
    if "99999" in out or "never" in out.lower():
        print("    [!] ALERT: rogueuser password never expires!")
        if auto_fix == 'y':
            print("    [+] REMEDIATING: Enforcing 90-day password expiry...")
            run_sudo_cmd("chage -M 90 rogueuser")
    # --- AUDIT 2: SUID Binaries ---
    print("\n[*] Scanning for illegal SUID binaries in /tmp...")
    out, err = run_sudo_cmd("find /tmp -perm -4000 -type f 2>/dev/null")
    
    if out:
        print(f"    [!] CRITICAL ALERT: SUID binary found at {out}")
        if auto_fix == 'y':
            print(f"    [+] REMEDIATING: Stripping SUID bit from {out}...")
            run_sudo_cmd(f"chmod u-s {out}")
    else:
        print("    [+] PASS: No dangerous SUID binaries found in /tmp.")
    # --- AUDIT 3: Immutable Locks ---
    print("\n[*] Verifying immutable locks on /etc/shadow...")
    out, err = run_sudo_cmd("lsattr /etc/shadow")
    
    if "-i-" in out:
        print("    [+] PASS: /etc/shadow is locked securely.")
    else:
        print("    [!] ALERT: /etc/shadow is missing the immutable flag!")
        if auto_fix == 'y':
            print("    [+] REMEDIATING: Applying immutable attribute...")
            run_sudo_cmd("chattr +i /etc/shadow")
    client.close()
    print("\n[*] Audit & Remediation Complete.")
except Exception as e:
    print(f"\n[!] Fatal Error: {e}")
