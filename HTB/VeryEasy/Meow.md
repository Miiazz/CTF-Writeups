#### Meow

**About:**  
Meow is a very easy Linux machine which guides players through setting up their attacking machine, connecting to HTB labs via VPN, and demonstrating the general strategy used to complete a box. The machine focuses on beginner enumeration techniques and showcases exploitation of a vulnerable Telnet service through default credentials.

**Process:**  
Connect using OpenVPN:

`sudo openvpn \~/path/to/downloaded/config`

The challenge itself provides the target IP as well as several general knowledge and retention questions, which are omitted from this write-up. One of the questions asks which service is running on port 23. To verify this, `nmap -p 23 <targetIP>` was used. The challenge then specifies that the root user is left without password protection. With this information, `telnet <targetIP> -l root` was used to establish a connection. From the home directory, `ls` was used to locate `flag.txt`, and `cat flag.txt` was used to read it.
