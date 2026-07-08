# Phase 4 — Automation Engineering (DevSecOps)

The manual remediation in Phase 2 is fine for a one-off lab, but it doesn't
scale past one box. This phase rebuilds the same checks as a script run
remotely from the attacker (Kali) machine over SSH, so the same audit can be
pointed at any number of hosts.

## 1. Install dependencies

```bash
sudo apt install python3-paramiko python3-nmap -y
```

- **Paramiko** — SSH client library, used to connect to and run commands on
  the target without an interactive session.
- **python3-nmap** — wraps `nmap` for host/port discovery.

## 2. Write the audit engine

`scripts/audit_engine.py` connects over SSH (key-based auth, via
Paramiko) to the target and checks the three vectors from Phase 1 that a
remote audit can realistically verify:

- **Account lifecycle** — runs `chage -l rogueuser` and flags it if the
  password is set to never expire (`99999`/"never").
- **SUID binaries** — runs `find /tmp -perm -4000 -type f` and flags any
  match.
- **Immutable lock on `/etc/shadow`** — runs `lsattr /etc/shadow` and
  checks for the `i` attribute.

It prompts once at startup — `Do you want to automatically remediate
vulnerabilities found? (y/n)` — and if you answer `y`, applies the
matching fix (`chage -M 90`, `chmod u-s`, `chattr +i`) for anything it
flags, using a small `run_sudo_cmd()` helper that pipes the sudo password
via `sudo -S` so it doesn't need an interactive TTY.

A practical note from building this: pasting multi-line code into `nano`
over an SSH session can trigger its auto-indent feature, which mixes tabs
and spaces and breaks Python's indentation-sensitive parsing. Pressing
`Alt+I` in `nano` toggles auto-indent off before pasting — worth doing
before pasting any script into a remote `nano` session.

## 3. Run it

```bash
python3 audit_engine.py
```

**Before running:** open the file and set `TARGET_IP`, `SSH_PORT`,
`USERNAME`, and `KEY_PATH` for your own lab, and set `SUDO_PASS` locally
on the machine you're running it from. Do not commit a real password into
that constant — treat `SUDO_PASS` as a placeholder to fill in at runtime,
not a value to check into git. If you want this to be safe to keep in a
public repo long-term, swap the hardcoded `SUDO_PASS` for a
`getpass.getpass()` prompt so no credential ever touches disk.

See [`scripts/audit_engine.py`](../scripts/audit_engine.py) for the full
implementation.

---

**Previous:** [03 — Perimeter Defense & Monitoring](./03-perimeter-and-monitoring.md)
**Next:** [05 — Verification](./05-verification.md)
