from fastapi import HTTPException, status

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

class InvitationExpiredException(HTTPException):
	def __init__(self, email):
		super().__init__(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail={
				"error_code": "INVITE_EXPIRED",
				"message": f"Invitation to {email} has already expired. Please contact the invitee."
			}
		)
