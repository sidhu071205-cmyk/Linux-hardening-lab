# Phase 5 — Verification & Kernel Mitigation

The last phase proves the defenses actually hold, using an independent
red-team tool rather than just re-checking my own work, and closes out a
couple of kernel-level findings that surfaced along the way.

## 1. Trigger the tripwire

```bash
sudo touch /etc/shadow
sudo ausearch -k shadow_changes
```

Attempts a trivial modification to `/etc/shadow` and confirms `auditd`
logs it under the `shadow_changes` key set up in Phase 3.

## 2. Independent red-team validation with LinPEAS

```bash
curl -L <linpeas_url> -o linpeas.sh
chmod +x linpeas.sh
./linpeas.sh
```

LinPEAS is a well-known Linux privilege-escalation enumeration script. Run
post-hardening, it found none of the rogue user, SUID binary, or ACL
backdoor from Phase 1 — confirming the file-level remediation held. It did
flag underlying kernel CVEs unrelated to the injected vectors, which the
next two steps address.

## 3. Blacklist vulnerable kernel modules

```bash
echo "install rxrpc /bin/false" | sudo tee /etc/modprobe.d/dirtyfrag-mitigation.conf
```

(repeated for `esp4` and `esp6`)

Maps the module's install hook to `/bin/false`. If anything — including an
attacker — tries to load the module, the load command exits immediately
with failure instead of loading vulnerable code.

## 4. Disable unprivileged user namespaces

```bash
sudo sysctl -w kernel.unprivileged_userns_clone=0
echo "kernel.unprivileged_userns_clone=0" | sudo tee -a /etc/sysctl.conf
```

Closes off a common privilege-escalation path (unprivileged namespace
cloning) that LinPEAS specifically checks for, and persists the setting
across reboots.

## 5. Final compliance score

```bash
sudo apt install lynis -y
sudo lynis audit system
```

Lynis runs several hundred individual checks across authentication,
filesystem, networking, and logging, and produces a **Hardening Index**.
This lab finished at **65** — solid for a general-purpose server baseline,
with Lynis's own suggestions log kept as a to-do list for further tightening
(e.g. further PAM tuning, additional logging destinations).

---

**Previous:** [04 — Automation Engineering](./04-automation.md)
**See also:** [Troubleshooting log](./troubleshooting.md)
