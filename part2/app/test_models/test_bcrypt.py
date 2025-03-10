from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Simuler un mot de passe en texte clair
password = "my_secure_password"

# Hachage du mot de passe
hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

# Vérification si le mot de passe correspond au haché
is_correct = bcrypt.check_password_hash(hashed_password, "my_secure_password")

print(f"Password hash: {hashed_password}")
print(f"Password matches: {is_correct}")
