from bot.db.db import *

with File(maintain_db) as db:
     data = db.get_invoices(user_nip='8943186123', month=False)

print(data)
