from cryptoamino.cipher.gioi import Gioi
from cryptoamino import tools

ptxt = "The world wonders"
cipher = Gioi()
ctxt = tools.concat(cipher.encrypt(ptxt))

print(ctxt)
