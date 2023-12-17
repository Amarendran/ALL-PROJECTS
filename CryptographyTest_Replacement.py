import enchant
def decrypt_message(encrypted_message):
    decrypted_message = ""
    for i in range(26):
        decrypted_message =""
        for letter in encrypted_message.lower():
            if letter.isalpha():
                if (ord(letter)+i>122):
                    decrypted_message += chr(ord(letter)+i-26)
                else:
                    decrypted_message += chr(ord(letter)+i)
            else:
                decrypted_message += letter
        print(decrypted_message,i)
    return decrypted_message

#decrypt_message("L olnh wr zhdu kdwv")
print(enchant.dict_exists('en_us'))
#d=enchant.Dict()

#print(d.tag)
print(enchant.dict_exists("en_US"))

#help(enchant)
#d =enchant.Dict("en_US")
print(enchant.check("Hello"))

#pre requisite
#apt install -y libenchant-dev
