from typing import Any


def response(
		status:int,
		description:str,
		example:Any
) -> dict:
	return {
		status:
		{
			'description':description,
			'content':
			{
				'application/json':
				{
					'example':example
				}
			}
		}
	}

def multi_response(
	status:int,
	description:str,
	examples:tuple[tuple[str,Any]]
) -> dict:
	try:
		return {
			status:
			{
				'description':description,
				'content':
				{
					'application/json':
					{
						'examples':
						{
							name:
							{
								'value':
								{
									'detail':value
								}
							}
							for name,value in examples
						}
					}
				}
			}
		}
	except ValueError:
		print(examples)
	exit()

def file_response(
	content_type:str
) -> dict:
	return {
		content_type:
		{
			'schema':
			{
				'type':'string',
				'format':'binary',
				'example':'binary file'
			}
		}
	}

def multi_file_response(
	status:int,
	description:str,
	content_types:tuple[str]
) -> dict:
	return {
		status:
		{
			'description':description,
			'content':
			{
				content_type:
				{
					'schema':
					{
						'type':'string',
						'format':'binary',
						'example':'binary file'
					}
				}
				for content_type in content_types
			}
		}
	}