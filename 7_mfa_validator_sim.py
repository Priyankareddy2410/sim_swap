import pyotp

totp = pyotp.TOTP('JBSWY3DPEHPK3PXP')  # base32 secret
print(" Authenticator App Code:", totp.now())

user_input = input("Enter code: ")
if user_input == totp.now():
    print(" Authenticated successfully")
else:
    print(" Invalid code. Access denied.")
