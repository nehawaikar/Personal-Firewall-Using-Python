\# Personal Firewall Using Python



A custom \*\*Personal Firewall application developed using Python\*\* for managing Windows Firewall rules and monitoring active network connections. The project provides a simple command-line interface to perform common firewall management and network monitoring tasks.



\## Project Overview



This project demonstrates how Python can be used to interact with the \*\*Windows Defender Firewall\*\* through Windows `netsh` commands.



The application allows users to create and remove firewall rules, block specific ports and IP addresses, block applications such as Google Chrome, monitor active network connections, and maintain a firewall activity log.



> \*\*Note:\*\* This project is designed for educational purposes and runs on Windows systems. Some operations require Administrator privileges.



\---



\## Objectives



The main objectives of this project are:



\* Block and unblock TCP/UDP ports

\*  Block and unblock specific IP addresses

\*  Block and unblock Google Chrome

\*  Monitor active network connections

\*  View existing Windows Firewall rules

\*  Check Windows Firewall status

\*  Maintain a firewall activity log

\*  Learn how Python interacts with Windows networking and security features



\---



\## Features



\### 1. Block Custom Port



Allows the user to block a specific TCP or UDP port using Windows Firewall rules.



\### 2. Unblock Custom Port



Removes a previously created firewall rule to allow traffic through the selected port.



\### 3. Block IP Address



Creates a Windows Firewall rule to block network traffic from a specified IP address.



\### 4. Unblock IP Address



Removes the firewall rule associated with a blocked IP address.



\### 5. Block Google Chrome



Creates a firewall rule to prevent Google Chrome from accessing the network.



\### 6. Unblock Google Chrome



Removes the Chrome blocking rule and restores network access.



\### 7. Monitor Active Connections



Uses `psutil` to display currently active network connections on the computer.



\### 8. View Firewall Rules



Displays existing Windows Firewall rules using the Windows `netsh` utility.



\### 9. Check Firewall Status



Checks whether Windows Defender Firewall is currently enabled or disabled.



\### 10. Activity Logging



Records important firewall actions and their timestamps in:



```text

firewall\_log.txt

```



\---



\## Technologies Used



| Technology                    | Purpose                                  |

| ----------------------------- | ---------------------------------------- |

| \*\*Python 3\*\*                  | Application development                  |

| \*\*Windows Defender Firewall\*\* | Network traffic filtering                |

| \*\*netsh\*\*                     | Windows Firewall command-line management |

| \*\*psutil\*\*                    | Monitoring active network connections    |

| \*\*subprocess\*\*                | Executing Windows system commands        |

| \*\*datetime\*\*                  | Recording timestamps in logs             |



\---



\## Requirements



Before running the project, make sure you have:



\* Windows 10 or Windows 11

\* Python 3.x

\* Administrator privileges

\* Internet connection for installing dependencies



\### Install Python



Download and install Python from the official Python website.



During installation, make sure \*\*"Add Python to PATH"\*\* is selected.



\### Install Required Library



Open Command Prompt or PowerShell and run:



```bash

pip install psutil

```



\---



\## How to Run



\### Step 1 — Clone or Download the Project



Download the project files to your computer.



\### Step 2 — Open the Project Folder



Open Command Prompt or PowerShell inside the project directory.



\### Step 3 — Run as Administrator



Because the application modifies Windows Firewall rules, open \*\*Command Prompt/PowerShell as Administrator\*\*.



\### Step 4 — Run the Python Program



```bash

python firewall.py

```



Replace `firewall.py` with the actual name of your Python file if it is different.



\---



\## Example Operations



The application provides options such as:



```text

1\. Block Custom Port

2\. Unblock Custom Port

3\. Block IP Address

4\. Unblock IP Address

5\. Block Google Chrome

6\. Unblock Google Chrome

7\. Monitor Active Connections

8\. View Firewall Rules

9\. Check Firewall Status

10\. Exit

```



The exact menu options may vary depending on the final version of the program.



\---



\## Firewall Activity Log



The application records firewall-related actions in:



```text

firewall\_log.txt

```



Example:



```text

\[2026-08-27 15:30:12] Blocked TCP port: 8080

\[2026-08-27 15:31:45] Blocked IP address: 192.168.1.100

\[2026-08-27 15:33:20] Firewall status checked

```



This makes it easier to track actions performed by the application.



\---





\## Security Considerations



\* The application should be executed with \*\*Administrator privileges\*\* when modifying firewall rules.

\* Only block IP addresses and ports that you understand and intend to block.

\* Incorrect firewall rules can affect network connectivity.

\* Avoid blocking essential Windows services or system ports.

\* Test firewall changes carefully before using them on an important system.



\---



\## Learning Outcomes



Through this project, I gained practical experience in:



\* Python system programming

\* Windows Firewall management

\* Network security concepts

\* TCP/UDP port management

\* IP address filtering

\* Network connection monitoring

\* Python `subprocess` usage

\* Python `psutil` library

\* Logging and activity tracking

\* Command-line system administration



\---





\## Disclaimer



This project is created for \*\*educational and cybersecurity learning purposes\*\*. It demonstrates basic interaction with Windows Firewall and network connections. Use it responsibly and only on systems that you own or have permission to administer.



\---



\## 👩‍💻 Author



\*\*Neha Waikar\*\*



\*\*Project:\*\* Personal Firewall Using Python



\*\*Technologies:\*\* Python • Windows Defender Firewall • netsh • psutil



\---



\## ⭐ Conclusion



The \*\*Personal Firewall Using Python\*\* project demonstrates how Python can be used to automate basic Windows Firewall management and network monitoring tasks.



It provides hands-on experience with \*\*network security, firewall rules, system commands, and Python-based automation\*\*, making it a practical cybersecurity project for learning

