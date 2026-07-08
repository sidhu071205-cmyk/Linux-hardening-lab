# Troubleshooting Log

Real errors hit while building this lab, why they happened, and how they
were fixed. Kept here rather than smoothed over, since the debugging is
often the most useful part for anyone repeating the exercise.

| Error | Root cause | Fix |
|---|---|---|
| `useradd`/`chpasswd` target typo (`rougeuser` vs `rogueuser`) | Simple spelling slip | Re-ran the command with the correct username |
| PAM rejected `password123` | The box's own `pwquality.conf` (configured earlier) correctly blocked a weak password | Used a password meeting the length/uppercase/symbol requirements |
| `Temporary failure resolving '...'` | VMware's NAT router restarted, breaking DNS resolution inside the VM | Set `nameserver 8.8.8.8` directly in `/etc/resolv.conf` as a stopgap, then ran `netplan apply` to restore normal resolution |
| `chattr: /etc/passwd/etc/shadow: No such file or directory` | Missing space between two file paths — the shell read it as one nested path | Added the missing space: `chattr +i /etc/passwd /etc/shadow` |
| `chmod: cannot access '/etc/cron.montly'` | Typo — missing the "h" in "monthly" | Corrected to `/etc/cron.monthly` |
| Python `IndentationError` on a pasted script | `nano`'s auto-indent mixed tabs and spaces when a multi-line block was pasted in | Reopened the file, pressed `Alt+I` in `nano` to disable auto-indent, then pasted again |
| Tried to `apt install` a module patch | Misread the LinPEAS module-hardening suggestion as an installable package rather than a config directive | Used `echo "install <module> /bin/false" | sudo tee ...` to write the correct modprobe directive instead |
| `sysctl: unknown key "kernal.unprivileged_userns_clone"` | Spelling error, "kernal" vs "kernel" | Corrected to `kernel.unprivileged_userns_clone=0` |
| Shell hung after a command with no visible prompt returning | An unclosed quote (`> "`) put the shell into multi-line input mode | Closed the quote and pressed Enter to return to a normal prompt, then re-ran the command |

These are left in deliberately — a hardening project that only shows clean,
first-try commands isn't a realistic account of how the work actually goes.
