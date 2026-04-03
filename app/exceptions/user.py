from fastapi import HTTPException

class UserNotFoundException(HTTPException):
	def __init__(self, email):
		super().__init__(
			status_code=404,
			detail={
				"error_code": "USER_NOT_FOUND",
				"message": f"User with email {email} does not exists."
			}
		)

class DuplicateEmailException(HTTPException):
	def __init__(self, email):
		super().__init__(
			status_code=409, 
			detail={
				"error_code": "DUPLICATE_EMAIL",
				"message": f"Email '{email}' is already registered.",
			})
