#### Redeemer

**About:**  
Redeemer is a very easy Linux machine which explores the enumeration and exploitation of a Redis database server while showcasing the `redis-cli` command-line utility and basic commands used to interact with the Redis service.

**Process:**  
An initial `nmap <targetIP>` revealed that all 1000 scanned ports were in ignored states. To investigate further, `nmap -p- -T5 <targetIP>` was used, revealing `redis` on port `6379`. `nmap -p 6379 -sV <targetIP>` identified the version as `Redis key-value store 5.0.7`.

`redis-cli -h <targetIP> -p 6379` was then used to connect to the Redis database. Once inside, `keys *` was used to list the keys, revealing one in position 3 named `flag`. `GET flag` was then used to display the flag.
