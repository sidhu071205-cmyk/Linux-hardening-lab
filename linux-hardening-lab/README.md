# Linux User & System Hardening Lab

A hands-on lab where I deliberately compromised an Ubuntu server with common
attack vectors (rogue accounts, SUID binaries, ACL backdoors, orphaned files),
then hunted down and remediated every one of them, hardened the kernel and
network stack, automated the audit with Python, and verified the result with
independent red-team tooling (LinPEAS) and a Lynis compliance score.

Everything here was run in a local lab environment: a Kali Linux attacker VM
against an Ubuntu Server VM, both on an isolated VMware network. **Do not run
any of the Phase 1 commands against a system you don't own or a network you
don't control.**

## Why this project

Most hardening guides only show the "after" picture. This lab is built the
other way around: inject a known vulnerability, prove it's exploitable,
remediate it, and prove the fix holds — using an independent scanner
(LinPEAS) and a scored audit (Lynis) as the final check rather than my own
say-so.

## Lab topology

- **Attacker:** Kali Linux VM
- **Target:** Ubuntu Server VM
- **Network:** VMware host-only/NAT network, isolated from production

## Structure

```
.
├── docs/
│   ├── 01-vulnerability-injection.md   # Red team: building the backdoors
│   ├── 02-system-hardening.md          # Blue team: filesystem & OS lockdown
│   ├── 03-perimeter-and-monitoring.md  # Firewall, kernel, audit tripwires
│   ├── 04-automation.md                # Python audit/remediation engine
│   ├── 05-verification.md              # LinPEAS + Lynis validation
│   └── troubleshooting.md              # Real errors hit along the way, and the fixes
├── scripts/
│   ├── audit_engine.py                 # Automated SSH-based audit & remediation
│   └── inject_vulnerabilities.sh       # Lab-only setup script (Phase 1)
└── LICENSE
```

## Results

| Metric | Result |
|---|---|
| Rogue accounts detected & removed | 1/1 |
| SUID backdoors detected & stripped | 1/1 |
| ACL backdoors detected & revoked | 1/1 |
| Orphaned files cleaned | 1/1 |
| LinPEAS findings post-hardening | No exploitable file/permission vectors found |
| Lynis hardening index | 65 |

## Skills demonstrated

- Linux user, permission, and ACL administration
- SUID/SGID and immutable-attribute (`chattr`) hardening
- `sysctl` / kernel parameter tuning
- UFW firewall policy design
- `auditd` rule-based file integrity monitoring
- Python + Paramiko for SSH-driven infrastructure automation
- Red-team validation using LinPEAS
- Compliance scoring using Lynis

## Disclaimer

This repository is for educational and portfolio purposes. The vulnerability
injection script is intended **only** for use in an isolated lab VM you own.

**Before pushing this repo anywhere:** `scripts/audit_engine.py` has a
`SUDO_PASS` constant near the top. Never fill that in with a real password
and commit it — treat it as a placeholder to set locally at runtime. If
you plan to keep this repo public long-term, swap it for a
`getpass.getpass()` prompt instead of a hardcoded string.
