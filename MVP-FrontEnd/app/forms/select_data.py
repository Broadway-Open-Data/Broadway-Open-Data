from flask_wtf import FlaskForm
from wtforms import StringField, DateField, BooleanField, IntegerField, SubmitField
from wtforms.fields import FormField, FieldList
from wtforms.validators import DataRequired

import datetime

# Make a form
class showInfo(FlaskForm):
    title = StringField(label='Show Name (fuzzy)')
    keyword = StringField(label='Keyword (fuzzy)')
    showId = IntegerField(label='ShowId')

class showGenre(FlaskForm):
    musicals = BooleanField(label="Musicals", default=True, render_kw ={'checked':''})
    plays = BooleanField(label="Plays", default=True, render_kw ={'checked':''})
    other_show_genre = BooleanField(label="Other", default=True, render_kw ={'checked':''})

class productionType(FlaskForm):
    originals = BooleanField(label="Originals", default=True, render_kw ={'checked':''})
    revivals = BooleanField(label="Revivals", default=True, render_kw ={'checked':''})
    other_production_type = BooleanField(label="Others", default=True, render_kw ={'checked':''})

class theatreInfo(FlaskForm):
    theatreName = StringField(label="Theatre Name (fuzzy)")
    theatreId = IntegerField(label="Theatre ID")

class dateRange(FlaskForm):
    # startDate = DateField(label="Start Date", description="this is a description", format='%Y-%m-%d', default=datetime.datetime(1850,1,1), validators=[DataRequired()])
    # endDate = DateField(label="End Date",format='%Y-%m-%d', default=datetime.datetime(2020,6,1))
    startYear = IntegerField(label="Start Year", default=1900, validators=[DataRequired()])
    endYear = IntegerField(label="End Year",default=2020, validators=[DataRequired()])

class summarizedFields(FlaskForm):
    """Some description."""
    # showInfoSum = FormField(showInfo, label="Show Info", description="hey", separator="-")
    showGenreSum = FormField(showGenre, label="Show Genre", description="hey")
    productionTypeSum = FormField(productionType, label="Production Type", description="hey")
    # theatreInfoSum = FormField(theatreInfo, label="Choose by Theatre Info",)
    dateRangeSum = FormField(dateRange, label="Choose by Date Range",)


# The acrtual form!
class dataForm(FlaskForm):
    """All of the fields as one."""
    allFields = FormField(summarizedFields)
    submit = SubmitField('Submit')
