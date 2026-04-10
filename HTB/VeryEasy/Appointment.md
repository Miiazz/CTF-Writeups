#### Appointment

**About:**  
Appointment is a very easy Linux machine which showcases beginner SQL injection techniques against a web application backed by an SQL database.

**Process:**  
`nmap <targetIP>` revealed that HTTP on port `80` was open and served `Apache httpd 2.4.38 ((Debian))`. Visiting `http://<targetIP>` in the browser revealed a login page. Up to this point, the challenge had already asked several free-form SQL injection questions, pointing toward an authentication bypass.

Using `admin'#` as the username with an invalid password successfully bypassed the login. This worked because the injected `'` closed the intended SQL string, while `#` commented out the remainder of the statement, effectively bypassing password validation.
