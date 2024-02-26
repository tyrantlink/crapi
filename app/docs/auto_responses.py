from app.utils.db.documents.ext.enums import AutoResponseMethod,AutoResponseType
from app.docs.helpers import response,multi_file_response,multi_response
from app.utils.db.documents import AutoResponse
from app.dependencies import BASE_URL
from typing import Literal

class AutoResponsesDocs:
  class AutoResponseDocsResponses:
    def __au_example(
      self,
      au_type:Literal['base','custom','unique','personal','mention']
    ) -> dict:
      match au_type:
        case 'base':
          return AutoResponse(
            id='b1',
            method=AutoResponseMethod.exact,
            trigger='trigger',
            response='response',
            type=AutoResponseType.text
          ).model_dump(mode='json')
        case 'custom':
          return AutoResponse(
            id='c1',
            method=AutoResponseMethod.contains,
            trigger='trigger',
            response='response',
            type=AutoResponseType.file,
            data=AutoResponse.AutoResponseData(
              custom=True,
              guild=123456789
            )
          ).model_dump(mode='json')
        case 'unique':
          return AutoResponse(
            id='u1',
            method=AutoResponseMethod.regex,
            trigger='trigger',
            response='response',
            type=AutoResponseType.script,
            data=AutoResponse.AutoResponseData(
              guild=123456789
            )
          ).model_dump(mode='json')
        case 'personal':
          return AutoResponse(
            id='p1',
            method=AutoResponseMethod.disabled,
            trigger='trigger',
            response='response',
            type=AutoResponseType.deleted,
            data=AutoResponse.AutoResponseData(
              user=123456789
            )
          ).model_dump(mode='json')
        case 'mention':
          return AutoResponse(
            id='m1',
            method=AutoResponseMethod.mention,
            trigger='123456789',
            response='response',
            type=AutoResponseType.text
          ).model_dump(mode='json')

    @property
    def get__au_id(self) -> dict:
      return {
        **multi_response
        (
          status = 200,
          description = 'auto response retrieved successfully',
          examples =
          (
            ('base auto response',self.__au_example('base')),
            ('custom auto response',self.__au_example('custom')),
            ('unique auto response',self.__au_example('unique')),
            ('personal auto response',self.__au_example('personal')),
            ('mention auto response',self.__au_example('mention'))
          )
        ),
        **response
        (
          status = 403,
          description = 'missing permissions',
          example =
          {
            'detail':'you do not have permission to access this auto response!'
          }
        ),
        **response
        (
          status = 404,
          description = 'auto response not found',
          example =
          {
            'detail':'auto response not found!'
          }
        )
      }

    @property
    def get__au_id__file(self) -> dict:
      return {
        **multi_file_response
        (
          status = 200,
          description = 'auto response file retrieved successfully',
          content_types =
          (
            'image/png',
            'video/mp4',
            'image/gif',
            'video/webm'
          )
        ),
        **response
        (
          status = 400,
          description = 'missing permissions',
          example =
          {
            'detail':'you do not have permission to access this auto response!'
          }
        ),
        **response
        (
          status = 404,
          description = 'auto response not found',
          example =
          {
            'detail':'auto response not found!'
          }
        ),
        **response
        (
          status = 500,
          description = 'invalid auto response category (this shouldn\'t happen unless there\'s something wrong with the database)',
          example =
          {
            'detail':'invalid auto response category `q`!'
          }
        )
      }

    @property
    def get__file__masked_url(self) -> dict:
      return {
        **multi_file_response
        (
          status = 200,
          description = 'auto response file retrieved successfully',
          content_types =
          (
            'image/png',
            'video/mp4',
            'image/gif',
            'video/webm'
          )
        ),
        **response
        (
          status = 400,
          description = 'invalid masked url',
          example =
          {
            'detail':'invalid masked url!'
          }
        ),
        **response
        (
          status = 404,
          description = 'auto response not found (this shouldn\'t happen unless something broke server side)',
          example =
          {
            'detail':'auto response not found!'
          }
        ),
        **response
        (
          status = 500,
          description = 'invalid auto response category (this shouldn\'t happen unless there\'s something wrong with the database)',
          example =
          {
            'detail':'invalid auto response category `q`!'
          }
        )
      }

    @property
    def post__au_id__masked_url(self) -> dict:
      return {
        200:
        {
          'description':'masked url created successfully!',
          'content':
          {
            'application/json':
            {
              'example':f'{BASE_URL}/au/file/QDWadh1ABL53KsNS'
            }
          }
        },
        **response
        (
          status = 200,
          description = 'masked url created successfully',
          example = f'{BASE_URL}/au/file/QDWadh1ABL53KsNS'
        ),
        **response
        (
          status = 403,
          description = 'missing permissions',
          example =
          {
            'detail':'you do not have permission to use this endpoint!'
          }
        )
      }

    @property
    def post__(self) -> dict:
      return {
        **multi_response
        (
          status = 200,
          description = 'auto response created successfully',
          examples =
          (
            ('base auto response',self.__au_example('base')),
            ('custom auto response',self.__au_example('custom')),
            ('unique auto response',self.__au_example('unique')),
            ('personal auto response',self.__au_example('personal')),
            ('mention auto response',self.__au_example('mention'))
          )
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
          status = 400,
          description = 'invalid auto response id',
          example =
          {
            'detail':'auto response id must be "unset"!'
          }
        )
      }

    @property
    def post__au_id__file(self) -> dict:
      return {
        **response
        (
          status = 200,
          description = 'file uploaded successfully',
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
        **multi_response
        (
          status = 400,
          description = 'invalid input',
          examples =
          (
            ('deleted auto response','you cannot upload a file to a deleted auto response!'),
            ('invalid file type','file must be a png, mp4, gif or webm!')
          )
        ),
        **response
        (
          status = 404,
          description = 'auto response not found',
          example =
          {
            'detail':'auto response not found!'
          }
        ),
        **response
        (
          status = 500,
          description = 'invalid auto response category (this shouldn\'t happen unless there\'s something wrong with the database)',
          example =
          {
            'detail':'invalid auto response category!'
          }
        )
      }

    @property
    def delete__au_id(self) -> dict:
      return {
        **response
        (
          status = 200,
          description = 'auto response deleted successfully',
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
        )
      }

    @property
    def patch__au_id(self) -> dict:
      return {
        **multi_response
        (
          status = 200,
          description = 'auto response updated successfully',
          examples =
          (
            ('base auto response',self.__au_example('base')),
            ('custom auto response',self.__au_example('custom')),
            ('unique auto response',self.__au_example('unique')),
            ('personal auto response',self.__au_example('personal')),
            ('mention auto response',self.__au_example('mention'))
          )
        ),
        **response
        (
          status = 403,
          description = 'missing permissions',
          example =
          {
            'detail':'you do not have permission to use this endpoint!'
          }
        )
      }
  
  class AutoResponseDocsRequests:
    ...

  responses = AutoResponseDocsResponses()