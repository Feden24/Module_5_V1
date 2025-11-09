message = "Hello World"

def checksum(msg):
    list = []
    list = msg.split()
    
    checked_list = []
    for word in list:
        checksum = sum(ord(c) for c in word) % 256
        checked_word = f"{word}:{checksum:02x}"
        checked_list.append(checked_word)
    return (checked_list)
    



if __name__ == "__main__":
    packet = checksum(message)
for word in packet:
    print(f"Sending packet: {word}")

