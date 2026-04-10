#### Dancing

**About:**  
Dancing is a very easy Windows machine which introduces the Server Message Block (`SMB`) protocol, its enumeration, and its exploitation when misconfigured to allow access without a password.

**Process:**  
Once connected to the machine, `nmap <targetIP>` revealed an `SMB` service, `microsoft-ds`, running on port `445`. Investigating further with `smbclient -L <targetIP>` revealed multiple hidden administrative shares (denoted by a `$` at the end) and one accessible share titled `WorkShares`. Connecting with `smbclient //<targetIP>/WorkShares` and then using `ls` revealed two users: `Amy.J` and `James.P`.

`cd Amy.J` followed by `ls` revealed `worknotes.txt`, which contained a reminder to set up and secure an Apache server. `cd James.P` followed by `ls` revealed `flag.txt`. `get flag.txt` was used to retrieve it, and `cat flag.txt` was used to view it.
