from mongoengine import (
    Document,
    StringField,
    ListField,
    EmbeddedDocumentField,
    EmbeddedDocument
)

class Replica(EmbeddedDocument):
    source = StringField(required=True, max_length=4)
    text = StringField(required=True)

class Dialog(EmbeddedDocument):
    created_at = StringField(required=True, max_length=100)
    replicas = ListField(required=True, field=EmbeddedDocumentField(Replica))

class DialogStorage(Document):
    session = StringField(required=True, max_length=50)
    dialogs = ListField(required=False, field=EmbeddedDocumentField(Dialog))

    meta = {
        'collection': 'dialog_storage'
    }