from fastapi import HTTPException, status

class CredentialsMismatchException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "CREDENTIAL_MISMATCH",
				"message": "The provided credential do not matches with our database",
			}
		)

class InvalidAccessTokenException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "INVALID_ACCESS_TOKEN",
				"message": "Could not validate the user"
			}
		)

class Invalid2FAException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "INVALID_2FA",
				"message": "OTP doesn't matches. Please try again.",
			}
		)

class ForbiddenAccessException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "FORBIDDEN_ACCESS",
				"message": "Access to the resource is forbidden.",
			}
		)