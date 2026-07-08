# Phase 2 — System Hardening & Remediation (Blue Team Defense)

With the vulnerabilities from Phase 1 in place, this phase hunts them down
and locks down the filesystem and resource limits more broadly.

## 1. Hunt and remediate SUID binaries

```bash
sudo find / -perm -4000 -type f 2>/dev/null
sudo chmod u-s /tmp/cp
```

`-perm -4000` finds every file with the SUID bit set; `2>/dev/null` discards
the noisy "permission denied" errors from directories a normal scan can't
read. `chmod u-s` strips the root-execution bit from the planted binary.

## 2. Remove hidden ACLs

```bash
getfacl /etc/shadow
sudo setfacl -x u:rogueuser /etc/shadow
```

`getfacl` surfaces ACL entries that `ls -l` would never show. `-x` removes
just the rogue entry rather than wiping the whole ACL.

## 3. Clean orphaned files

```bash
sudo find / -nouser 2>/dev/null
sudo rm /tmp/orphan_payload.sh
```

`-nouser` finds files owned by a UID with no corresponding account.

## 4. Apply immutable locks to critical files

```bash
sudo chattr +i /etc/passwd /etc/shadow
lsattr /etc/passwd
```

The `+i` (immutable) attribute is enforced at the filesystem/kernel level —
even `root` cannot modify, delete, rename, or append to the file until the
attribute is removed. This is a deliberate trade-off: it also means you have
to remember to `chattr -i` before legitimately editing these files (e.g.
adding a new user), which is worth calling out in the repo since it trips
people up in production.

## 5. Restrict permissions on newly created files

Edited `/etc/login.defs`:

```
UMASK 027
```

`027` means new files get no permissions at all for "other," tightening the
default from Ubuntu's typical `022`.

## 6. Secure shared memory

Edited `/etc/fstab`:

```
tmpfs /dev/shm tmpfs defaults,noexec,nodev,nosuid 0 0
```

```bash
sudo systemctl daemon-reload
sudo mount -o remount /dev/shm
```

`/dev/shm` is a common target for fileless malware because it's
world-writable by default. `noexec` blocks anything from being executed
there directly; `nosuid` ignores SUID/SGID bits on anything placed there.

## 7. Lock down cron

```bash
sudo chown root:root /etc/crontab
sudo chmod 600 /etc/crontab
sudo chmod -R 700 /etc/cron.*
```

Restricts both viewing and scheduling of system-wide automated tasks to
root.

## 8. Prevent resource exhaustion

Edited `/etc/security/limits.conf`:

```
* hard core 0
* hard nproc 1000
```

`core 0` disables core dumps system-wide (core dumps can leak in-memory
credentials); `nproc 1000` caps per-user process count as a fork-bomb
mitigation.

---

**Previous:** [01 — Vulnerability Injection](./01-vulnerability-injection.md)
**Next:** [03 — Perimeter Defense & Monitoring](./03-perimeter-and-monitoring.md)
