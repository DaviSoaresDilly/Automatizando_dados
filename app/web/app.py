# app/web/app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from app.database import get_session
from app.reports.generate_reports import generate_atendimentos_report, export_report_to_csv
from app.database.update_data import update_atendimento_status, update_paciente_info
from app.web.forms import UpdateAtendimentoForm  # Importar formulário para validação
from flask_caching import Cache

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Necessário para CSRF Protection e Forms

csrf = CSRFProtect(app)  # Proteger a aplicação com CSRF
cache = Cache(app, config={'CACHE_TYPE': 'simple'})  # Configuração de Cache

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/relatorios')
def relatorios():
    session = get_session()
    df = generate_atendimentos_report(session)
    filename = "atendimentos_report.csv"
    export_report_to_csv(df, filename)
    session.close()
    return render_template('relatorios.html', filename=filename, table=df.to_html(classes="table"))

@app.route('/relatorios_cache')
@cache.cached(timeout=60)
def relatorios_cache():
    session = get_session()
    df = generate_atendimentos_report(session)
    session.close()
    return render_template('relatorios.html', table=df.to_html(classes="table"))

@app.route('/atualizar_atendimento', methods=['GET', 'POST'])
def atualizar_atendimento():
    form = UpdateAtendimentoForm()  # Instanciar o formulário
    if form.validate_on_submit():  # Validar formulário via WTForms
        atendimento_id = form.atendimento_id.data
        status = form.status.data
        session = get_session()
        if update_atendimento_status(session, atendimento_id, status):
            session.close()
            return redirect(url_for('index'))
        session.close()
    return render_template('atualizar_atendimento.html', form=form)

@app.route('/atualizar_paciente', methods=['GET', 'POST'])
def atualizar_paciente():
    if request.method == 'POST':
        paciente_id = int(request.form['paciente_id'])
        nome = request.form['nome']
        idade = int(request.form['idade'])
        session = get_session()
        if update_paciente_info(session, paciente_id, nome=nome, idade=idade):
            session.close()
            return redirect(url_for('index'))
        session.close()
    return render_template('atualizar_paciente.html')

if __name__ == "__main__":
    app.run(debug=True)
