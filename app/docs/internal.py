from app.docs.helpers import response

class InternalDocs:
	@property
	def post__reload_au(self) -> dict:
		return {
			**response
			(
				status = 200,
				description = 'auto response reloaded successfully',
				example =
				{
					'success':True
				}
			),
			**response
			(
				status = 403,
				description = 'missing permissions',
				example =
				{
					'detail':'you do not have permission to use this endpoint!'
				}
			),
			**response
			(
				status = 503,
				description = 'not all clients responded!',
				example =
				{
					'detail':'not all clients responded!'
				}
			)
		}