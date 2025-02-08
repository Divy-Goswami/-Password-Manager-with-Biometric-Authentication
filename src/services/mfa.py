import pyotp

def generate_secret():
    """Generate a secret key for TOTP."""
    return pyotp.random_base32()

def verify_otp(secret, otp):
    """Verify the OTP entered by the user."""
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)