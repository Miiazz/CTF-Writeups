# PicoCTF Write-Ups 2026

## Environment

These challenges were completed on a Lenovo ThinkPad E14 running Linux Mint with i3.  
For access to tooling better suited to forensic and pentesting work, I used a Kali XFCE virtual machine, especially for challenges involving SSH or other remote access.

---

## General Skills

### SUDO MAKE ME A SANDWICH

Points: 50

Summary:  
Can the flag be read, and if so, how?

Notes:  
I ran ls -la to inspect the directory contents and found flag.txt, but elevated permissions were required to read it. Running sudo -l showed that emacs could be executed as root. Using that privilege, I opened the file with sudo emacs flag.txt and retrieved the flag.

---

### Piece by Piece

Points: 50

Summary:  
After logging in, multiple file fragments are present in the home directory. These parts must be combined to recover the flag.

Notes:  
I found several numbered files in the home directory and used cat file\* > flag.txt to combine them into a single output, which revealed the flag. Note: file\* is a placeholder for the actual file names.

---

### Password Profiler

Points: 100

Summary:  
Using OSINT-style personal details about a target, generate a custom password list and recover the original password by matching its hash.

Notes:  
Personal information was provided in userinfo.txt. I used those details with CUPP to generate a targeted wordlist, then used that list to crack the provided password hash with the provided check_password script.

---

### MultiCode

Points: 200

Summary:  
A suspiciously encoded message contains a hidden flag under multiple layers of obfuscation such as ROT13, URL encoding, HEX, and Base64.

Notes:  
I used CyberChef to peel back multiple layers of encoding until the flag was revealed.

---

### ping-cmg

Points: 100

Summary:  
Can you make the server reveal its secrets? The service appears to only allow pinging Google DNS.

Notes:  
Connecting to the host revealed a ping service aimed at 8.8.8.8. Testing showed that 127.0.0.1 also worked, which indicated that inputs were not verified to strictly 8.8.8.8 and that there was potential to gather insights about the host. This created a suspicion that command injection was possible: 127.0.0.1; ls revealed flag.txt, and 127.0.0.1; cat flag.txt displayed the flag.

---

### Printer Shares

Points: 50

Summary:  
Someone accidentally sent an important file to a network printer. The goal is to retrieve it from the print server.

Notes:  
The challenge provided the printer domain and port. From there, smbclient -L //mysterious-sea.picoctf.net/ -p 56429 was used without a username or password to list available shares. This revealed a guest-accessible share named shares. With that in mind, smbclient //mysterious-sea.picoctf.net/shares -p 56429 -N was used to connect. From within the SMB prompt, ls was used to identify flag.txt, and get flag.txt was used to download it.

---

### Printer Shares 2

Points: 200

Summary:  
A secure printer is now in use. I’m confident no one can leak the message again... or can you?

Notes:  
Because the challenge indicated that there were two printers on the network, one public and one secure, I began with smbclient -L //green-hill.picoctf.net/ -p 61943 to list available shares. This revealed both a public shares share and an internal secure-shares share. I first connected to the public share with smbclient //green-hill.picoctf.net/shares -p 61943 -U guest. Running ls revealed three text files: content.txt, kafka.txt, and notification.txt. While content.txt and kafka.txt appeared to be normal print jobs, notification.txt contained a note addressed to Joe advising use of the other printer with default credentials. I then tested access to the secure share with smbclient //green-hill.picoctf.net/secure-shares -p 61943 -U Joe, which confirmed that the Joe account existed but required a password. To recover it, I used nxc smb green-hill.picoctf.net -u Joe -p \~/Documents/rockyou.txt --port 61943 --ignore-pw-decoding, which revealed popcorn as the password. Using the username Joe and password popcorn granted access to the secure share, where ls revealed flag.txt. I downloaded it with get flag.txt and read the flag locally.

---

### Printer Shares 3

Points: 300

Summary:  
I accidentally left the debug script in place… Well, I think that's fine - No one could possibly access my super secure directory

Notes:  
I again started with smbclient -L //dolphin-cove.picoctf.net/ -p 62531 to identify the available shares. That revealed a public share, so I connected with smbclient //dolphin-cove.picoctf.net/shares -p 62531 -U guest. Running ls showed script.sh and cron.log, and I used get to pull both files. Reading them with cat made it clear from the timestamps that the script was running on a timer.

To test whether the script was writable and usable, I modified script.sh to include:

```bash
find / -name "flag*" 2>/dev/null >> /proc/self/cwd/cron.log
```

After uploading it back with put and letting it run, the updated cron.log showed /challenge/secure-shares/flag.txt, which I retrieved again with get cron.log. From there, I updated the script a second time to include:

```bash
cat /challenge/secure-shares/flag.txt >> /proc/self/cwd/cron.log
```

After waiting for the script to execute and pulling the updated cron.log, reading the log revealed the flag.

---

### KSECRETS

Points: 100

Summary:  
We have a Kubernetes cluster setup and flag is in the secrets. You think you can get it?

Notes:  
Using the provided .yml file, I ran the following command to list secrets:

```bash
kubectl --kubeconfig=kubeconfig.yaml --server=https://green-hill.picoctf.net:51989 --insecure-skip-tls-verify get secrets -A
```

This revealed a picoctf namespace. The use of --insecure-skip-tls-verify was suggested by the challenge and made sense given the login prompt behavior.

Since Kubernetes secrets are Base64-encoded, I then used:

```bash
kubectl --kubeconfig=kubeconfig.yaml --server=https://green-hill.picoctf.net:51989 --insecure-skip-tls-verify get secret ctf-secret -n picoctf -o jsonpath='{.data.flag}' | base64 -d
```

to decode the flag.

---

## Web Exploitation

### Old Sessions

Points: 100

Summary:  
A poorly designed social media site stores session information insecurely. The goal is to gain elevated access by reusing an exposed session.

Notes:  
I used Inspect > Developer Tools > Storage to inspect cookies. A browser extension like Cookie-Editor could also work, but it was not necessary. After creating an account, I found a post referencing a /sessions page containing session data. Replacing my current session cookie with one found there and refreshing the page granted admin access.

---

### Secret Box

Points: 200

Summary:  
This secret box is designed to conceal your secrets. It's perfectly secure—only you can see what's inside. Or can you?

Notes:  
Initial SQLi attempts against the login page were unsuccessful, and Burp Suite scans did not immediately reveal anything useful. Investigating the source with grep -rn login revealed that app/src/server.js handled the login logic. While most values were protected, one line in the app.post('/secrets/create') function stood out:

```sql
INSERT INTO secrets(owner_id, content) VALUES ('${userId}', '${content}')
```

That suggested the content field was injectable through the secret creation dialog. From there, I created an account, navigated to the create new secrets page, and began testing payloads. Initial attempts failed due to column fitting, but using concatenation with the following payload:

```sql
' || (SELECT content FROM secrets WHERE owner_id = 'e2a66f7d-2ce6-4861-b4aa-be8e069601cb' LIMIT 1) || '
```

resolved the issue and revealed the flag.

---

### Hashgate

Points: 100

Summary:  
See if you can gain access to the admin panel of this website and remember obfuscation is not always security.

Notes:  
Inspection of the site's source revealed a comment showing guest credentials. Logging in with them revealed a note which disclosed the guest ID as 3000 and the URL that contained /profile/user/e93028bdc1aacdfb3687181f2031765d an ID that appeared to be an MD5 hash of 3000. With this information paired with the knowledge that there are only 20 employees within the organization, a Python script was used to loop through and generate hashes from 2980-3021 and append that value after the /user/ segment of the URL. When the script completed it returned a string containing the flag.

---

## Forensics

### Disko-4

Points: 200

Summary:  
Find a deleted file within a disk image.

Notes:  
The challenge provided a gzipped disk image. After extracting it, I obtained disko-4.dd. I used sudo testdisk disko-4.dd and followed the menus None > Image Creation > Undelete, which revealed two deleted files: messages and dont-delete.gz. After recovering dont-delete.gz, I extracted it and used cat on the recovered file to reveal the flag.

---

### Forensics Git 0

Points: 200

Summary:  
Can you find the flag in this disk image?

Notes:  
The challenge provided a gzipped disk image. After extracting it, I obtained disk.img. I used sudo testdisk disk.img and followed the menus Intel > Analyze > Backup to inspect the Linux partition. Navigating to /home/ctf-player/Code/secrets revealed notes.txt, but reading it showed only the picoCTF{} wrapper, making it a likely red herring. That led me to inspect the hidden .git directory inside secrets. Running ls -la revealed COMMIT_EDITMSG, and reading that file exposed the leetspeak text needed to complete the flag.

---

### Forensics Git 1

Points: 300

Summary:  
Can you find the flag in this disk image?

Notes:  
Similarly, this challenge provided a gzipped disk image. Following gunzip, I used sudo testdisk disk.img for initial analysis, where a home directory was found and copied for further investigation. This revealed a hidden .git directory. Running git log showed that the flag had been added and later removed through commits. After noting the hash of the initial commit where the flag was introduced, sudo git restore --source 177789af0b300e043ea8f54ea57d6cee352291ae -- . was run from the project root to restore and read flag.txt.

---

### Forensics Git 2

Points: 400

Summary:  
The agents interrupted the perpetrators’ disk deletion routine. Can you recover this Git repo?

Notes:  
Similar to Forensics Git 1, the challenge provided a gzipped disk image. After extracting it, I used sudo testdisk disk.img for initial analysis. Once a home directory was recovered and copied for further investigation, I navigated to ctf-player/Code/killer-chat-app. From there, I inspected the hidden .git directory. Reading ../.git/logs/HEAD with cat revealed recent commit activity, including a commit labeled Add secret hideout chat log with the hash e80b38b3322a5ba32ac07076ef5eeb4a59449875. That suggested the deleted content could be restored from that commit. Running sudo git restore --source e80b38b3322a5ba32ac07076ef5eeb4a59449875 -- . from the project root restored the missing files, including a text file in the application logs that contained the flag.

---

### Rogue Tower

Points: 300

Summary:  
A suspicious cell tower has been detected in the network. Analyze the captured network traffic to identify the rogue tower, find the compromised device, and recover the exfiltrated flag.

Notes:  
Analysis of the .pcap revealed multiple GET and POST requests originating from 10.100.55.55 and going to 198.51.100.244. Following the TCP stream on the initial GET request and viewing it in UTF-8 revealed IMSI:310410275849303, which, per the challenge, is what the encryption key is derived from.

Following the HTTP stream for the POST requests revealed normal headers along with data transfers of either nine or three bytes. Translating the transferred bytes from hex produced the string R1xbW3pndkhFBV9BCmxTAFtZZ0AJRANBaAIBBloEAQUASA==. The trailing == suggested Base64 padding, but decoding it directly did not produce anything useful.

That pointed toward an additional layer of encoding. Since IMSI values are often involved in XOR-based challenge logic, I tested different substrings of the IMSI as the key. Using the last 8 digits, 75849303, in UTF-8 produced readable output and led to the recovered flag.

---

### Binary Digits

Points: 100

Summary:  
A file full of 1s and 0s or is there more?

Notes:  
Inspecting the file with file showed that it was a bin file and therefore contained binary data. Uploading it to CyberChef and using From Binary revealed that it was an image, as indicated by the JFIF header. From there, selecting Render Image Raw revealed the flag.

---

## Reverse Engineering

### Silent Stream

Points: 200

Summary:  
We recovered a suspicious packet capture file that seems to contain a transferred file. The sender also shared the script used to encode and send it. Can you reconstruct the original file?

Notes:  
Opening the provided .pcap in Wireshark revealed a TCP conversation, and the raw data was extracted via Follow TCP Stream > Save as Raw into tcp.txt. The provided encryption.py script showed that each byte was encoded using (b + key) % 256 with a key of 42. Based on that logic, I created decrypt.py to reverse the operation by subtracting the key from each byte modulo 256.

After running python3 decrypt.py, I used file decrypted to identify the recovered data, which turned out to be a JPEG image. Renaming it via mv to decrypted.jpg and opening it revealed the flag.
