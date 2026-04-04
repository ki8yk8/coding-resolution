from pyotp import TOTP, random_base32

def create_secret()->str:
	return random_base32()

def generate_qr_URI(email: str, secret: str)->str:
	totp = TOTP(secret)
	uri = totp.provisioning_uri(name=email, issuer_name="MOSAIC")
	
	return uri

def verify_totp(secret: str, code: int)->bool:
	totp = TOTP(secret)
	return totp.verify(code)
