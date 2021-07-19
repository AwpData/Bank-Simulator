# Bank-Simulator
Bank simulation with account numbers and pins. Created to refresh Python knowledge and learn how databases work.

<h1> Features </h1>
<li>Random valid credit card numbers using the <a href="https://www.geeksforgeeks.org/luhn-algorithm/">Luhn Algorithm</a></li>
<li>Random PIN numbers for security</li>
<li>Able to add money to balance</li>
<li>Can transfer money between two accounts</li>
<li>Credit cards are stored in SQLite database</li>
<br><br>
SQLite database is created under the file name *'card.s3db'*, but you can store to local memory if you want.
<br><br>
`conn = sqlite3.connect(":memory:")`
