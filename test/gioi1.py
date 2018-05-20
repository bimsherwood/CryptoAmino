from cryptoamino.cipher.gioi1 import Gioi1
from cryptoamino import tools

ptxt = "The world wonders"
cipher = Gioi1()

ctxt = tools.concat(cipher.encrypt(ptxt))
print(ctxt)

recovered = tools.concat(cipher.decrypt(ctxt))
print(recovered)
