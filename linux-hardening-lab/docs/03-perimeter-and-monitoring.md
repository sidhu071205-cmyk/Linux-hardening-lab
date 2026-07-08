# Phase 3 — Perimeter Defense & Active Monitoring

With the filesystem hardened, this phase locks down the network boundary
and sets up tripwires to catch intrusion attempts as they happen.

## 1. Configure the UFW firewall

```bash
sudo ufw default deny incoming
sudo ufw allow 2222/tcp
sudo ufw enable
```

Default-deny for all inbound traffic, with a single explicit allow for SSH
on a non-standard port (2222 instead of 22, to cut down on automated
scanner noise).

## 2. Tune kernel network parameters

Edited `/etc/sysctl.conf`:

```
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
```

```bash
sudo sysctl -p
```

- `accept_redirects = 0` — ignores ICMP redirect messages, which can be used
  to silently reroute traffic through an attacker.
- `log_martians = 1` — logs packets with impossible/spoofed source
  addresses instead of silently dropping them.
- `icmp_echo_ignore_broadcasts = 1` — mitigates Smurf-style broadcast
  amplification attacks.

## 3. Establish audit tripwires

```bash
sudo apt install auditd -y
sudo auditctl -w /etc/shadow -p wa -k shadow_changes
```

`auditd` watches (`-w`) `/etc/shadow` for writes and attribute changes
(`-p wa`), and tags matching log entries with a searchable key
(`-k shadow_changes`) so they're easy to pull out of a large audit log
later with `ausearch -k shadow_changes`.

---

**Previous:** [02 — System Hardening](./02-system-hardening.md)
**Next:** [04 — Automation Engineering](./04-automation.md)
