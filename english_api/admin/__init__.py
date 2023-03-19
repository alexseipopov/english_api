from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from english_api import app, db
from english_api.models.models import Group, User, Word

admin = Admin(app, url='/admin', template_mode='bootstrap4')


class WordAdminView(ModelView):
    column_list = ("id", "word_en", "word_ru", "example", "audio_path", "image_path", "group_id")
    form_columns = ("word_en", "word_ru", "example", "audio_path", "image_path", "group")
    form_ajax_refs = {
        "group": {
            "fields": ("label",)
        }
    }
    column_searchable_list = ("word_en", "word_ru")


class GroupAdminView(ModelView):
    column_list = ("label", "level")
    form_columns = ("label", "level")
    column_searchable_list = ("label",)


admin.add_view(ModelView(User, db.session))
admin.add_view(GroupAdminView(Group, db.session))
admin.add_view(WordAdminView(Word, db.session))
