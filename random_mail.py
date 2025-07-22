import random

# ตัวอักษรที่ใช้ในคำ
vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

def generate_word():
    # สร้างคำที่มีสระรวมอยู่ด้วย ขนาด 3 ตัวอักษร
    word = random.choice(consonants) + random.choice(vowels) + random.choice(consonants)
    return word

def generate_email_and_password():
    first_name = generate_word() + generate_word()
    last_name = generate_word() + generate_word()
    number = random.randint(100, 999)

    email = f"{first_name}{number}@hotmail.com"
    password = f"{first_name}_{number}"

    return email, password, first_name, last_name

# เขียนไฟล์
with open("infomail.txt", "w") as file:
    for _ in range(20):
        email, password, first_name, last_name = generate_email_and_password()
        file.write(f"{email}\n")
        file.write(f"{password}\n")
        file.write(f"{first_name}\n")
        file.write(f"{last_name}\n\n")

print("save infomail.txt")
