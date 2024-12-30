from django.shortcuts import render
from copy import deepcopy
from minions import (
    generate_session
)
from rest_framework.views import (
    APIView,
    Response
)
from .serializers import (
    DialogStorage as DialogStorageSerializer
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter
)

class DialogStorage(APIView):
    serializer_class = DialogStorageSerializer
    http_method_names = ['get', 'post', 'delete']
    response_json = {
        'status': 'error',
        'errors': []
    }

    @extend_schema(
            parameters=[
                OpenApiParameter(name='dialog_index', type=str, required=False)
            ]
    )
    def get(self, request, *args, **kwargs):
        response_json = deepcopy(self.response_json)

        try:
            session = request.COOKIES.get('session')
            dialog_index = request.GET.get('dialog_index')

            if not session: 
                raise Exception('Session didn\'t find')
    
            dialogs = self.serializer_class.get_dialogs(session=session, dialog_index=dialog_index)
            response_json['dialogs'] = dialogs
            response_json['status'] = 'success'

        except (Exception, ) as e:
            if hasattr(e, 'detail'):
                response_json['errors'] = e.detail
            else:
                response_json['errors'].append(str(e))

        finally:
            return Response(
                response_json
            )
        
    @extend_schema(
        request=DialogStorageSerializer
    )
    def post(self, request, *args, **kwargs):
        response_json = deepcopy(self.response_json)

        try:
            session = request.COOKIES.get('session')
            if not session: 
                raise Exception('Session didn\'t find')

            data = request.data
            data['session'] = session
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            response_json['status'] = 'success'

        except (Exception, ) as e:
            if hasattr(e, 'detail'):
                response_json['errors'] = e.detail
            else:
                response_json['errors'].append(str(e))

        finally:
            return Response(
                response_json
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(name='dialog_index', type=str, required=True)
        ]
    )
    def delete(self, request, *args, **kwargs):
        response_json = deepcopy(self.response_json)

        try:
            session = request.COOKIES.get('session')
            if not session: 
                raise Exception('Session didn\'t find')

            dialog_index = request.GET.get('dialog_index')
            self.serializer_class.delete_dialog(session=session, dialog_index=dialog_index)
            response_json['status'] = 'success'

        except (Exception, ) as e:
            if hasattr(e, 'detail'):
                response_json['errors'] = e.detail
            else:
                response_json['errors'].append(str(e))

        finally:
            return Response(
                response_json
            )

def chat_page(request):
    session = request.COOKIES.get('session')
    if not session:
        session = generate_session()

    dialogs = DialogStorageSerializer.get_dialogs(session=session).get('dialogs', [])
    response = render(
        request=request,
        template_name='chatpage.html',
        context={
            'session': session,
            'dialogs': list(enumerate(dialogs))
        }
    )

    response.set_cookie('session', session)
    return response


