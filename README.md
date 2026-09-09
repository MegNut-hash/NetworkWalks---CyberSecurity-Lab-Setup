# NetworkWalks — CyberSecurity Lab Setup

**Kali Linux setup routed through Oracle VirtualBox, for cybersecurity testing.**

---

## Overview

This repo documents how I built my cybersecurity homelab. The main goal was a safe, reproducible, and repeatable environment that can run scanning, enumeration, and exploitation tools without putting my home network in jeopardy — and one I can trace back to a clean installation if need be.

The lab sits on its own NAT Network, so I can drop in additional target VMs later and have them communicate with Kali Linux, without exposing anything over at my home internet.

---

## 🎯 Objectives

- Install VirtualBox and import a Kali Linux VM
- Build an isolated NAT Network for the lab
- Configure Kali's network adapter and assign it a consistent IP
- Confirm connectivity, gateway routing, and DNS resolution
- Take a clean snapshot as a recovery baseline
- Document the process, including what went wrong

---

## Why an Isolated Lab?

Running security tools against live networks or systems that I am not given access to is illegal. So this lab exists so that I can practice reconnaissance, scanning, and exploitation against machines I control, inside a set network boundary that can't go anywhere else.

**This lab is for systems I own or have explicit permission to test only.**

---

## ⚙️ Lab Configuration

| Component | Configuration |
|---|---|
| Host OS | Windows 11 Home |
| Host RAM | 32 GB |
| Hypervisor | VirtualBox 7.2.16 |
| Guest OS | Kali Linux 2026.2 |
| Guest RAM | 4096 MB |
| Guest CPUs | 2 |
| Guest Storage | 80.09 GB (SATA, VMDK) |
| Network Adapter | Intel PRO/1000 MT Desktop |
| Virtual Network | NAT Network (`NatNetwork`) |
| Network Range | 10.0.0.0/24 |
| Kali IP | 10.0.0.2/24 |
| Gateway | 10.0.0.1 |
| DNS | 8.8.8.8 |

---

# 🪜 Setup Steps

## 1. Install VirtualBox

Installed VirtualBox 7.2.16 as the hypervisor on the host.

## 2. Build the NAT Network

Created a dedicated NAT Network in VirtualBox rather than using the default NAT adapter, since a NAT Network lets multiple VMs on the same network talk to each other while still routing out — a plain NAT adapter isolates each VM from the others.

**[Screenshot: NAT Network settings — network name, IPv4 prefix, DHCP]**

## 3. Import Kali Linux

Downloaded the Kali Linux VM image from the official site and imported it into VirtualBox.

**[Screenshot: VM details pane — the one you just uploaded]**

Key config:
- Base Memory: 4096 MB
- Processors: 2
- Storage: `kali-linux-2026.2-vmware-amd64.vmdk` (80.09 GB)
- Adapter 1: Intel PRO/1000 MT Desktop, attached to NAT Network (`NatNetwork`)

## 4. Configure Kali's Network

Set a consistent IP on Kali via NetworkManager (IPv4 Settings → Manual) so it's easy to reference in future exercises instead of relying on whatever DHCP hands out.

**[Screenshot: NetworkManager IPv4 Settings — address 10.0.0.2, netmask 24, gateway 10.0.0.1, DNS 8.8.8.8]**

Confirmed the config took effect on the command line:

```
$ ip a
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:90:20:68 brd ff:ff:ff:ff:ff:ff
    inet 10.0.0.2/24 brd 10.0.0.255 scope global noprefixroute eth0
```

**[Screenshot: terminal output of `ip a` + `ping google.com`]**

## 5. Take a Clean Snapshot

Snapshotted the VM once networking was confirmed working, so I always have a baseline to roll back to after breaking something during an exercise.

Snapshot name: *[fill in]*

---

# 🔎 Verification

| Test | Command | Result |
|---|---|---|
| IP address | `ip a` | ✅ `10.0.0.2/24` shown on `eth0` |
| Internet reachable | `ping 8.8.8.8` | ✅ 0% packet loss, avg ~17ms |
| Domain resolves (ping) | `ping google.com` | ✅ resolved and replied |
| DNS resolution | `nslookup google.com` | ✅ resolved via `8.8.8.8#53` |
| Nmap installed | `nmap --version` | ✅ Nmap 7.99 |
| Snapshot restores cleanly | Restore + `ip a` | ✅ baseline config comes back |

**[Screenshot: `ping 8.8.8.8` + `nslookup google.com` output]**
**[Screenshot: `nmap --version` output]**

---

# 🐞 Problems & Fixes

## Problem 1: Internet dropped after setting a static IP

After switching the Wired connection's IPv4 method to Manual and setting the static address, Kali temporarily lost internet connectivity — a known issue with how NetworkManager handles duplicate address detection (DAD) on some setups.

Fix:
```
sudo nmcli connection modify "Wired connection 1" ipv4.dad-timeout 0
```
Restarted the connection and connectivity came back.

> Connection names can differ between installs — check yours first with `nmcli connection show` before running the modify command.

## Problem 2: VirtualBox wouldn't start the VM (VT-x error)

VirtualBox refused to boot the Kali VM, throwing a virtualization error. Hardware virtualization was disabled in the host's BIOS/UEFI.

Fix:
1. Rebooted into BIOS/UEFI
2. Enabled Intel VT-x
3. Saved and rebooted
4. VM booted normally after that

---

# 💡 What I Learned

- **NAT vs NAT Network:** a plain NAT adapter gives each VM its own private network with no visibility between VMs; a NAT Network lets VMs on it see each other while still getting outbound access — that's what makes multi-VM lab setups possible.
- **VM resource allocation:** matched CPU/RAM to what Kali actually needs rather than over-provisioning, since this is running alongside other work on the host.
- **Static IP configuration:** setting a fixed address makes it much easier to document and reference the machine later, instead of chasing a DHCP lease.
- **Snapshots as a safety net:** always take one before doing anything that could break the config — it turns "I broke my lab" into a 30-second fix.

---

# 🔗 Tools & Resources

- **VirtualBox:** <https://virtualbox.org/wiki/Downloads>
- **Kali Linux:** <https://kali.org/get-kali>

---

# 👤 Author

**Niluxan**
Computer Science with Cyber Security, Royal Holloway, University of London

---

## 📌 Project Info

**Week:** 1 | **Project:** Cybersecurity Lab Setup
