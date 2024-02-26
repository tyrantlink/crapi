_openapi_tag_map = {}
def insert_tag(index:int,tag:dict) -> list:
	global _openapi_tag_map
	_openapi_tag_map[index] = tag
	_openapi_tag_map = dict(sorted(_openapi_tag_map.items()))
	return list(_openapi_tag_map.values())