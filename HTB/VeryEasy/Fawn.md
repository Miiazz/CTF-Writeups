#### Fawn

**About:**
Fawn is a very easy Linux machine which explores the File Transfer Protocol (FTP) and its exploitation when misconfigured to allow anonymous access.

**Process:**  
Once connected to the machine, the challenge instructions and free-form questions indicated a focus on FTP. To follow this trail, `nmap -sV <targetIP>` was used to verify the service and version. From there, an anonymous login was attempted via `ftp <targetIP>` using anonymous as the username and a blank password. This attempt was successful, and `ls` revealed `flag.txt`. get `flag.txt` was then used to download the flag, and `cat flag.txt` was used to read it.
