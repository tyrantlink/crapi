from app.docs.helpers import response

class GeneralDocs:
	@property
	def get__(self) -> dict:
		return {
			**response
			(
				status = 200,
				description = 'simple root endpoint',
				example = 'crab api, for use with /reg/nal and /reg/nal derivatives.'
			)
		}

	@property
	def get__version(self) -> dict:
		return {
			**response
			(
				status = 200,
				description = 'version of the api',
				example = '1.0.0'
			)
		}