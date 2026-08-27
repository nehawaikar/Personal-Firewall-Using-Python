import subprocess
import psutil
import os
import ipaddress
import ctypes
from datetime import datetime


# ============================================================
# PERSONAL FIREWALL
# Python + Windows Defender Firewall
# ============================================================

LOG_FILE = "firewall_log.txt"


# ============================================================
# LOG FILE
# ============================================================

def log_action(action):

    try:
        log_path = os.path.abspath(LOG_FILE)

        with open(log_path, "a", encoding="utf-8") as log_file:

            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            log_file.write(
                f"[{current_time}] {action}\n"
            )

    except Exception as e:

        print(f"\nLogging error: {e}")


# ============================================================
# ADMINISTRATOR CHECK
# ============================================================

def is_admin():

    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

    except Exception:
        return False


# ============================================================
# CHECK FIREWALL COMMAND AVAILABILITY
# ============================================================

def firewall_command_available():

    try:

        result = subprocess.run(
            ["netsh", "advfirewall", "show", "allprofiles"],
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    except Exception:
        return False


# ============================================================
# RUN WINDOWS FIREWALL COMMAND
# ============================================================

def run_cmd(command):

    print("\n----------------------------------------")
    print("Executing command:")
    print(command)
    print("----------------------------------------")

    try:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print("\nCommand executed successfully.")

            if result.stdout.strip():
                print(result.stdout)

            log_action(
                f"SUCCESS: {command}"
            )

            return True

        else:

            print("\nCommand failed.")

            if result.stderr.strip():

                print("\nError:")
                print(result.stderr)

            log_action(
                f"FAILED: {command} | "
                f"{result.stderr.strip()}"
            )

            return False

    except Exception as e:

        print(f"\nError executing command: {e}")

        log_action(
            f"ERROR executing command: {command} | {e}"
        )

        return False


# ============================================================
# VALIDATE PORT
# ============================================================

def validate_port(port):

    if not port.isdigit():

        return False

    return 1 <= int(port) <= 65535


# ============================================================
# SELECT PROTOCOL
# ============================================================

def select_protocol():

    print("\nSelect Protocol")
    print("1. TCP")
    print("2. UDP")

    choice = input(
        "Enter your choice (1-2): "
    ).strip().upper()

    if choice in ("1", "TCP"):
        return "TCP"

    if choice in ("2", "UDP"):
        return "UDP"

    print("\nInvalid protocol choice.")

    log_action(
        f"INVALID protocol selected: {choice}"
    )

    return None


# ============================================================
# SELECT DIRECTION
# ============================================================

def select_direction():

    print("\nSelect Traffic Direction")
    print("1. Outbound")
    print("2. Inbound")

    choice = input(
        "Enter your choice (1-2): "
    ).strip()

    if choice == "1":
        return "out"

    if choice == "2":
        return "in"

    print("\nInvalid direction.")

    log_action(
        f"INVALID direction selected: {choice}"
    )

    return None


# ============================================================
# BLOCK CUSTOM PORT
# ============================================================

def block_custom_port():

    port = input(
        "\nEnter port number to block: "
    ).strip()

    if not validate_port(port):

        print(
            "\nInvalid port number."
            "\nPort must be between 1 and 65535."
        )

        log_action(
            f"INVALID PORT entered for blocking: {port}"
        )

        return

    protocol = select_protocol()

    if protocol is None:
        return

    direction = select_direction()

    if direction is None:
        return

    direction_name = (
        "Outbound"
        if direction == "out"
        else "Inbound"
    )

    rule_name = (
        f"PersonalFirewall_Block_"
        f"{protocol}_{direction_name}_Port_{port}"
    )

    command = (
        f'netsh advfirewall firewall add rule '
        f'name="{rule_name}" '
        f'dir={direction} '
        f'action=block '
        f'protocol={protocol} '
        f'localport={port} '
        f'enable=yes'
    )

    if run_cmd(command):

        print(
            f"\nBlocked {protocol} port {port} "
            f"({direction_name})."
        )


# ============================================================
# UNBLOCK CUSTOM PORT
# ============================================================

def unblock_custom_port():

    port = input(
        "\nEnter port number to unblock: "
    ).strip()

    if not validate_port(port):

        print(
            "\nInvalid port number."
        )

        log_action(
            f"INVALID PORT entered for unblocking: {port}"
        )

        return

    protocol = select_protocol()

    if protocol is None:
        return

    direction = select_direction()

    if direction is None:
        return

    direction_name = (
        "Outbound"
        if direction == "out"
        else "Inbound"
    )

    rule_name = (
        f"PersonalFirewall_Block_"
        f"{protocol}_{direction_name}_Port_{port}"
    )

    command = (
        f'netsh advfirewall firewall delete rule '
        f'name="{rule_name}"'
    )

    run_cmd(command)


# ============================================================
# FIND GOOGLE CHROME
# ============================================================

def find_chrome():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ]

    for path in chrome_paths:

        if os.path.exists(path):

            return path

    return None


# ============================================================
# BLOCK GOOGLE CHROME
# ============================================================

def block_chrome():

    chrome_path = find_chrome()

    if chrome_path is None:

        print(
            "\nGoogle Chrome was not found."
        )

        log_action(
            "FAILED: Google Chrome executable not found"
        )

        return

    print("\nGoogle Chrome found:")
    print(chrome_path)

    rule_name = "PersonalFirewall_Block_Chrome"

    command = (
        f'netsh advfirewall firewall add rule '
        f'name="{rule_name}" '
        f'dir=out '
        f'action=block '
        f'program="{chrome_path}" '
        f'enable=yes'
    )

    if run_cmd(command):

        print(
            "\nGoogle Chrome outbound traffic blocked."
        )


# ============================================================
# UNBLOCK GOOGLE CHROME
# ============================================================

def unblock_chrome():

    rule_name = "PersonalFirewall_Block_Chrome"

    command = (
        f'netsh advfirewall firewall delete rule '
        f'name="{rule_name}"'
    )

    run_cmd(command)


# ============================================================
# VALIDATE IP ADDRESS
# ============================================================

def validate_ip(ip_address):

    try:

        ipaddress.ip_address(ip_address)

        return True

    except ValueError:

        return False


# ============================================================
# BLOCK IP ADDRESS
# ============================================================

def block_ip():

    ip_address = input(
        "\nEnter IPv4/IPv6 address to block: "
    ).strip()

    if not validate_ip(ip_address):

        print(
            "\nInvalid IP address."
        )

        log_action(
            f"INVALID IP entered: {ip_address}"
        )

        return

    direction = select_direction()

    if direction is None:
        return

    direction_name = (
        "Outbound"
        if direction == "out"
        else "Inbound"
    )

    safe_ip = ip_address.replace(":", "_").replace(".", "_")

    rule_name = (
        f"PersonalFirewall_Block_IP_"
        f"{direction_name}_{safe_ip}"
    )

    command = (
        f'netsh advfirewall firewall add rule '
        f'name="{rule_name}" '
        f'dir={direction} '
        f'action=block '
        f'remoteip={ip_address} '
        f'enable=yes'
    )

    if run_cmd(command):

        print(
            f"\nIP address {ip_address} blocked."
        )


# ============================================================
# UNBLOCK IP ADDRESS
# ============================================================

def unblock_ip():

    ip_address = input(
        "\nEnter IP address to unblock: "
    ).strip()

    if not validate_ip(ip_address):

        print(
            "\nInvalid IP address."
        )

        log_action(
            f"INVALID IP entered for unblocking: {ip_address}"
        )

        return

    direction = select_direction()

    if direction is None:
        return

    direction_name = (
        "Outbound"
        if direction == "out"
        else "Inbound"
    )

    safe_ip = ip_address.replace(":", "_").replace(".", "_")

    rule_name = (
        f"PersonalFirewall_Block_IP_"
        f"{direction_name}_{safe_ip}"
    )

    command = (
        f'netsh advfirewall firewall delete rule '
        f'name="{rule_name}"'
    )

    run_cmd(command)


# ============================================================
# VIEW FIREWALL RULES
# ============================================================

def view_rules():

    print(
        "\n========== FIREWALL RULES ==========\n"
    )

    command = [
        "netsh",
        "advfirewall",
        "firewall",
        "show",
        "rule",
        "name=all"
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():

            print(result.stdout)

        if result.stderr.strip():

            print("\nError:")
            print(result.stderr)

        log_action(
            "Viewed Windows Firewall rules"
        )

    except Exception as e:

        print(
            f"\nError viewing firewall rules: {e}"
        )

        log_action(
            f"ERROR viewing firewall rules: {e}"
        )


# ============================================================
# MONITOR NETWORK CONNECTIONS
# ============================================================

def monitor_connections():

    print(
        "\n========== ACTIVE NETWORK CONNECTIONS ==========\n"
    )

    try:

        connections = psutil.net_connections(
            kind="inet"
        )

        print(
            f"{'Protocol':<10}"
            f"{'Local Address':<28}"
            f"{'Remote Address':<28}"
            f"{'Status':<15}"
            f"{'PID'}"
        )

        print("-" * 100)

        connection_count = 0

        for conn in connections:

            if conn.type == 1:

                protocol = "TCP"

            elif conn.type == 2:

                protocol = "UDP"

            else:

                protocol = "OTHER"

            if conn.laddr:

                local_address = (
                    f"{conn.laddr.ip}:"
                    f"{conn.laddr.port}"
                )

            else:

                local_address = "-"

            if conn.raddr:

                remote_address = (
                    f"{conn.raddr.ip}:"
                    f"{conn.raddr.port}"
                )

            else:

                remote_address = "-"

            status = conn.status or "-"

            pid = conn.pid if conn.pid else "-"

            print(
                f"{protocol:<10}"
                f"{local_address:<28}"
                f"{remote_address:<28}"
                f"{status:<15}"
                f"{pid}"
            )

            connection_count += 1

        print(
            f"\nTotal connections: "
            f"{connection_count}"
        )

        log_action(
            f"Viewed active network connections "
            f"({connection_count} connections)"
        )

    except Exception as e:

        print(
            "\nError monitoring network traffic:"
        )

        print(e)

        log_action(
            f"ERROR monitoring traffic: {e}"
        )


# ============================================================
# FIREWALL STATUS
# ============================================================

def firewall_status():

    print(
        "\n========== WINDOWS FIREWALL STATUS ==========\n"
    )

    command = [
        "netsh",
        "advfirewall",
        "show",
        "allprofiles"
    ]

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():

            print(result.stdout)

        if result.stderr.strip():

            print("\nError:")
            print(result.stderr)

        log_action(
            "Checked Windows Firewall status"
        )

    except Exception as e:

        print(
            f"\nError checking firewall status: {e}"
        )

        log_action(
            f"ERROR checking firewall status: {e}"
        )


# ============================================================
# VIEW FIREWALL LOG
# ============================================================

def view_log():

    print(
        "\n========== FIREWALL ACTIVITY LOG ==========\n"
    )

    log_path = os.path.abspath(LOG_FILE)

    print(
        f"Log file location:\n{log_path}\n"
    )

    print("-" * 70)

    try:

        with open(
            log_path,
            "r",
            encoding="utf-8"
        ) as log_file:

            content = log_file.read()

            if content.strip():

                print(content)

            else:

                print(
                    "Firewall activity log is empty."
                )

    except FileNotFoundError:

        print(
            "No firewall activity has been logged yet."
        )

    except Exception as e:

        print(
            f"\nError reading firewall log: {e}"
        )


# ============================================================
# CLEAR FIREWALL LOG
# ============================================================

def clear_log():

    confirm = input(
        "\nAre you sure you want to clear the log? "
        "(Y/N): "
    ).strip().upper()

    if confirm != "Y":

        print(
            "\nOperation cancelled."
        )

        return

    try:

        with open(
            LOG_FILE,
            "w",
            encoding="utf-8"
        ):
            pass

        print(
            "\nFirewall log cleared."
        )

        log_action(
            "Firewall log cleared"
        )

    except Exception as e:

        print(
            f"\nError clearing log: {e}"
        )


# ============================================================
# FIREWALL INITIALIZATION CHECK
# ============================================================

def startup_check():

    print(
        "\n=============================================="
    )

    print(
        "        PERSONAL FIREWALL INITIALIZATION"
    )

    print(
        "=============================================="
    )

    if is_admin():

        print(
            "\n[+] Administrator privileges detected."
        )

        log_action(
            "Administrator privileges detected"
        )

    else:

        print(
            "\n[!] WARNING:"
        )

        print(
            "    This program is NOT running as Administrator."
        )

        print(
            "    Firewall rule changes may fail."
        )

        log_action(
            "WARNING: Program started without administrator privileges"
        )

    if firewall_command_available():

        print(
            "[+] Windows Firewall is accessible."
        )

        log_action(
            "Windows Firewall command verified"
        )

    else:

        print(
            "[!] Unable to access Windows Firewall."
        )

        log_action(
            "WARNING: Windows Firewall command unavailable"
        )


# ============================================================
# MAIN MENU
# ============================================================

def main():

    startup_check()

    log_action(
        "Personal Firewall program started"
    )

    while True:

        print("\n")
        print("==============================================")
        print("              PERSONAL FIREWALL")
        print("==============================================")
        print("1.  Block Custom Port")
        print("2.  Unblock Custom Port")
        print("3.  Block Google Chrome")
        print("4.  Unblock Google Chrome")
        print("5.  Block IP Address")
        print("6.  Unblock IP Address")
        print("7.  View Firewall Rules")
        print("8.  Monitor Network Traffic")
        print("9.  View Firewall Log")
        print("10. Clear Firewall Log")
        print("11. Firewall Status")
        print("12. Exit")
        print("==============================================")

        choice = input(
            "Enter your choice (1-12): "
        ).strip()

        if choice == "1":

            block_custom_port()

        elif choice == "2":

            unblock_custom_port()

        elif choice == "3":

            block_chrome()

        elif choice == "4":

            unblock_chrome()

        elif choice == "5":

            block_ip()

        elif choice == "6":

            unblock_ip()

        elif choice == "7":

            view_rules()

        elif choice == "8":

            monitor_connections()

        elif choice == "9":

            view_log()

        elif choice == "10":

            clear_log()

        elif choice == "11":

            firewall_status()

        elif choice == "12":

            print(
                "\nExiting Personal Firewall..."
            )

            log_action(
                "Personal Firewall program exited"
            )

            break

        else:

            print(
                "\nInvalid choice!"
            )

            print(
                "Please enter a number from 1 to 12."
            )

            log_action(
                f"Invalid menu choice entered: {choice}"
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
