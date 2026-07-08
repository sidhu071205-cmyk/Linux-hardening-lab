#!/usr/bin/env bash
#
# inject_vulnerabilities.sh
#
# LAB-ONLY setup script. Deliberately introduces the vulnerabilities
# documented in docs/01-vulnerability-injection.md so they can be hunted
# down and remediated in Phase 2.
#
# DO NOT run this against any system other than a disposable lab VM you
# own and control, on a network you own and control (e.g. an isolated
# VMware host-only network). Running this against a shared, production,
# or internet-facing system will create real, exploitable security holes.
#
# Usage: sudo ./inject_vulnerabilities.sh

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "This script must be run as root (sudo ./inject_vulnerabilities.sh)." >&2
  exit 1
fi

read -r -p "This will intentionally weaken this machine's security for lab purposes. Type 'yes' to continue: " CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
  echo "Aborted."
  exit 0
fi

echo "[1/6] Creating backdoor account 'rogueuser'..."
useradd -m -s /bin/bash rogueuser || true
echo 'rogueuser:Password1234!' | chpasswd

echo "[2/6] Granting passwordless sudo to rogueuser..."
echo 'rogueuser ALL=(ALL) NOPASSWD:ALL' | tee /etc/sudoers.d/rogueuser
chmod 440 /etc/sudoers.d/rogueuser

echo "[3/6] Disabling password aging for rogueuser..."
chage -M 99999 rogueuser

echo "[4/6] Planting SUID binary at /tmp/cp..."
cp /bin/cp /tmp/cp
chmod 4755 /tmp/cp

echo "[5/6] Installing acl tools and adding hidden ACL backdoor on /etc/shadow..."
apt-get update -qq
apt-get install -y acl >/dev/null
setfacl -m u:rogueuser:rw /etc/shadow

echo "[6/6] Leaving an orphaned payload file (owned by nonexistent UID 9999)..."
touch /tmp/orphan_payload.sh
chown 9999:9999 /tmp/orphan_payload.sh

echo
echo "Done. Vulnerabilities injected:"
echo "  - rogue user account with passwordless sudo and no password expiry"
echo "  - SUID binary at /tmp/cp"
echo "  - hidden ACL grant on /etc/shadow for rogueuser"
echo "  - orphaned file owned by a nonexistent UID at /tmp/orphan_payload.sh"
echo
echo "Proceed to Phase 2 (docs/02-system-hardening.md) to hunt and remediate these."
