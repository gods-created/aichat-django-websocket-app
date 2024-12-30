from rest_framework.serializers import (
    Serializer,
    CharField,
    ListField,
    ChoiceField
)
from models import (
    DialogStorage as DialogStorageModel,
    Dialog as DialogModel
)
from enum import Enum
from minions import (
    row_to_json,
)

class Source(Enum):
    USER = 'user'
    AI = 'ai'

class ReplicaField(Serializer):
    source = ChoiceField(
        required=True, 
        choices=[
            (v.value, v.value) for v in Source
        ],
        error_messages = {
            'required': 'The \'source\' field is required'
        }
    )

    text = CharField(
        required=True,
        min_length=1,
        error_messages = {
            'required': 'The \'text\' field is required',
            'min_length': 'The \'text\' field has to have min. 1 character'
        }
    )

class DialogField(Serializer):
    created_at = CharField(
        required=True, 
        max_length=100,
        error_messages = {
            'required': 'The \'created_at\' field is required',
            'max_length': 'The \'created_at\' field has to have max. 100 characters'
        }
    )

    replicas = ListField(
        child=ReplicaField(),
        allow_empty=False,
        min_length=1,
        error_messages = {
            'allow_empty': 'The \'replicas\' field can\'t to be empty',
            'min_length': 'The \'replicas\' field has to have min. 1 value'
        }
    )

class DialogStorage(Serializer):
    session = CharField(
        required=True,
        min_length=1,
        max_length=50,
        error_messages = {
            'required': 'The \'session\' field is required',
            'min_length': 'The \'session\' field has to have min. 1 character',
            'max_length': 'The \'session\' field has to have max. 50 characters'
        }
    )

    dialog = DialogField(
        required=True,
        error_messages = {
        'required': 'The \'dialog\' field is required',
        }
    )
    
    @staticmethod
    def get_dialogs(**kwargs):
        session = kwargs.get('session')
        dialog_index = kwargs.get('dialog_index')
        
        if not session:
            return []
        
        row = DialogStorageModel.objects(session=session).first()
        if not row:
            return {}
        
        item = row_to_json(row)
        if dialog_index:
            try:
                dialog_index = int(dialog_index)
                item['dialogs'] = [
                    item['dialogs'][dialog_index]
                ]
            except Exception as e:
                pass

        return item
    
    @staticmethod
    def delete_dialog(**kwargs):
        session = kwargs.get('session')
        dialog_index = kwargs.get('dialog_index')
        if not all((session, dialog_index)):
            return
        
        row = DialogStorageModel.objects(session=session).first()
        if not row:
            return
        
        try:
            dialog_index = int(dialog_index)
        except:
            return

        if len(row.dialogs) == 1:
            row.delete()
        else:
            del row.dialogs[
                dialog_index
            ]
            row.save()

        return

    def create(self, validated_data):
        session = validated_data.get('session')
        dialog = validated_data.get('dialog')
        item = DialogStorageModel.objects(session=session).first()

        if not item:
            del validated_data['dialog']
            item = DialogStorageModel(**validated_data)

        item.dialogs.append(DialogModel(**dialog))  
        item.save()
        return row_to_json(item)
