from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField

from english_api import app, db
from english_api.models.models import Group, User, Word

admin = Admin(app, url='/admin', template_mode='bootstrap4')


class WordAdminView(ModelView):
    column_list = ("id", "word_en", "word_ru", "example_ru", "example_en", "transcription", "audio_path", "image_path", "group_id")
    form_columns = ("word_en", "word_ru", "example_ru", "example_en", "transcription", "audio_path", "image_path", "group")
    form_ajax_refs = {
        "group": {
            "fields": ("label",)
        }
    }
    form_overrides = {
        "audio_path": FileUploadField,
        "image_path": FileUploadField
    }
    form_args = {
        "audio_path": {
            "label": "Аудио файл",
            "base_path": app.config["UPLOAD_FOLDER_AUDIO"]
        },
        "image_path": {
            "label": "Изображение",
            "base_path": app.config["UPLOAD_FOLDER_IMAGE"]
        }
    }
    column_searchable_list = ("word_en", "word_ru")

    def on_model_change(self, form, model, is_created):
        if is_created:
            # for i in form:
            #     print(i.value)
            print(model.group_id)


class GroupAdminView(ModelView):
    column_list = ("label", "level")
    form_columns = ("label", "level")
    column_searchable_list = ("label",)


# TODO убрать на деплое - это служебная информация
admin.add_view(ModelView(User, db.session))

admin.add_view(GroupAdminView(Group, db.session))
admin.add_view(WordAdminView(Word, db.session))
