from app.docs.helpers import response,multi_response
from app.utils.db.documents import User

class UserDocs:
	@property
	def get__user_id(self) -> dict:

		normal_user = User(
			id = 123456789,
			username = 'normal user',
			config = User.UserConfig
			(
				tts = User.UserConfig.UserConfigTTS
				(
					name = 'display name'
				)
			),
			data = User.UserData
			(
				api = User.UserData.UserDataAPI
				(
					token = '$2b$12$RIOA11rvynaMyv4yTJhw6.1o.k6cZ6nuNxz3AQA5IfT/D4tayg4kO'
				),
				auto_responses = User.UserData.UserDataAutoResponses
				(
					found = ['b1','b2','c13']
				),
				statistics = User.UserData.UserDataStatistics
				(
					messages = {
						'_legacy':12345,
						'844127424526680084':1234
					}
				),
				dm_threads = {
					'853783693628669952':1211192508688891924,
					'1069890280347676742':1211241487619325972
				}
			)
		).model_dump(mode='json')
		return {
			**multi_response
			(
				status = 200,
				description = 'user data retrieved successfully',
				examples =
				(
					('normal user',normal_user),
				)
			),
			**response
			(
				status = 403,
				description = 'missing permissions',
				example =
				{
					'detail':'you do not have permission to access this user!'
				}
			),
			**response
			(
				status = 404,
				description = 'user not found',
				example =
				{
					'detail':'user not found!'
				}
			)
		}

	@property
	def post__user_id__reset_token(self) -> dict:
		return {
			**response
			(
				status = 200,
				description = 'token reset successfully',
				example = 'dV1YNSN=nb.BE4irLl.Eneuxe01lPhmk6c0bvMW50KpB5E'
			),
			**response
			(
				status = 403,
				description = 'missing permissions',
				example =
				{
					'detail':'you do not have permission to access this user!'
				}
			),
			**response
			(
				status = 404,
				description = 'user not found',
				example =
				{
					'detail':'user not found!'
				}
			)
		}