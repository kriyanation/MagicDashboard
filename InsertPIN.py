import sqlite3
import tkinter
from  tkinter import simpledialog
import bcrypt

root = tkinter.Tk()

pin = simpledialog.askstring("PIN","Enter PIN",parent=root)
connection = sqlite3.connect("MagicCheck")
theone = pin.encode('utf-8')
salt = bcrypt.gensalt()
hashed=bcrypt.hashpw(theone,salt)
pin_encrypted = hashed
cur = connection.cursor()
sql = "update Check_Teacher set PIN=?"
cur.execute(sql, (pin_encrypted,))
connection.commit()
sql = "select PIN from Check_Teacher"
cur.execute(sql)
pin = cur.fetchone()[0]
thetwo = "AA1010".encode('utf-8')
print(bcrypt.checkpw(thetwo,pin))

root.mainloop()
