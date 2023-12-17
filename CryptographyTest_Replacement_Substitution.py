import enchant

def Shift(i,letter):
    decrypted_message =""
    if letter.isalpha():
        if (ord(letter)+i>122):
            decrypted_message += chr(ord(letter)+i-26)
        else:
            decrypted_message += chr(ord(letter)+i)
    else:
        decrypted_message += letter        
    
    return decrypted_message

def decrypt_message(encrypted_message):
    decrypted_message = ""
    for i in range(26):
        for j in range(26):
            decrypted_message =""
            encrypted_message=encrypted_message.lower()
            if encrypted_message.isalpha():
                decrypted_message += Shift(i,encrypted_message[0])
                decrypted_message += Shift(j,encrypted_message[1])
            print(decrypted_message,i,j)
    return decrypted_message

#decrypt_message("L olnh wr zhdu kdwv")

decrypt_message("EV")