# app/web/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class UpdateAtendimentoForm(FlaskForm):
    atendimento_id = IntegerField('ID do Atendimento', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Concluído', 'Concluído'), ('Em andamento', 'Em andamento'), ('Cancelado', 'Cancelado'), ('Aguardando', 'Aguardando')])

class UpdatePacienteForm(FlaskForm):
    paciente_id = IntegerField('ID do Paciente', validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    idade = IntegerField('Idade', validators=[NumberRange(min=0, max=120)])
