from fastmcp import FastMCP
from typing import Optional
import os

from db import init_db, track_whoa, count_whoa, last_reason

# Inisialisasi DB saat startup
init_db()

app = FastMCP("whoa-mcp")

@app.tool()
def whoAmI(username: str) -> dict:
  """
  Mengembalikan identitas user.
  """
  return {
    "username": username,
    "message": f"Your username is {username}"
  }

@app.tool()
def trackWhoa(username: str, reason: Optional[str] = "Probably some AI stuff") -> dict:
  """
  Simpan event 'whoa' untuk user tertentu dengan alasan.
  """
  if not username:
    raise ValueError("username is required")
  track_whoa(username, reason or "Probably some AI stuff")
  return {
    "ok": True,
    "message": f"{username} said whoa and it was tracked",
    "username": username,
    "reason": reason
  }

@app.tool()
def reportWhoaCount(username: str) -> dict:
  """
  Kembalikan jumlah 'whoa' untuk user.
  """
  total = count_whoa(username)
  last = last_reason(username)
  return {
    "username": username,
    "whoa_count": total,
    "last_reason": last
  }

if __name__ == "__main__":
  # Jalankan via SSE supaya bisa diakses pakai URL (localhost:8000)
  port = int(os.getenv("PORT", "8000"))
  app.run("sse", host="0.0.0.0", port=port)
