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
