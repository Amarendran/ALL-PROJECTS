
def character_2_Enum(sampletext):
    char_seen = []
    categorization=[]
    for i, c in enumerate(sampletext):
        #print (i, c)
        if not c in char_seen:
            categorization.append(len(char_seen))
            char_seen.append(c)
        else:
            for j, ca in enumerate(char_seen):
                if c==ca:
                    #print (j, ca)
                    categorization.append(j)
    return('.'.join(str(e) for e in categorization))

print(character_2_Enum('tetest'))
