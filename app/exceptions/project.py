from fastapi import HTTPException, status

class ProjectNotFoundException(HTTPException):
	def __init__(self, id: str):
		super().__init__(
			status_code=status.HTTP_404_NOT_FOUND,
			detail={
				"error_code": "PROJECT_NOT_FOUND",
				"message": f"The project '{id}' you are looking for doesn't exists or has been deleted."
			}
		)

class AlreadySharedException(HTTPException):
	def __init__(self, id:str, email: str):
		super().__init__(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail={
				"error_code": "ALREADY_SHARED",
				"message": f"Project {id} has already been shared with {email}."
			}
		)

class OnlyAuthorCanShareException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "ONLY_ADMIN_CAN_SHARE",
				"message": f"Project access can be only granted by the project author"
			}
		)

class OnlyAuthorCanDeleteException(HTTPException):
	def __init__(self):
		super().__init__(
			status_code=status.HTTP_403_FORBIDDEN,
			detail={
				"error_code": "ONLY_ADMIN_CAN_DELETE",
				"message": f"Any project only can be deleted by its author."
			}
		)
