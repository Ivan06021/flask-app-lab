from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateTimeLocalField,
    SelectField,
    SelectMultipleField,
    StringField,
    TextAreaField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length
from app.posts.models import Tag

CATEGORIES = [
    ("tech", "Technology"),
    ("science", "Science"),
    ("lifestyle", "Lifestyle"),
]


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(2)])
    content = TextAreaField(
        "Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()]
    )
    is_active = BooleanField("Active Post")
    publish_date = DateTimeLocalField("Publish Date", format="%Y-%m-%dT%H:%M")
    category = SelectField("Category", choices=CATEGORIES,
                           validators=[DataRequired()])
    author_id = SelectField('Author', coerce=int)
    tags = SelectMultipleField('Tags', coerce=int)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    submit = SubmitField("Add Post")
