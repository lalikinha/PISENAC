from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "chave_secreta"

# Configuração do MySQL
app.config['MYSQL_HOST'] = '108.181.223.38'
app.config['MYSQL_USER'] = 'userSenac'
app.config['MYSQL_PASSWORD'] = 'biamontalvao'
app.config['MYSQL_DB'] = 'ProjetoSenac'

mysql = MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('gerenciamento'))

@app.route('/gerenciamento')
def gerenciamento():
    # Recuperar dados das três tabelas
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM profissao")
    profissoes = cursor.fetchall()

    cursor.execute("SELECT * FROM profissional")
    profissionais = cursor.fetchall()

    cursor.execute("SELECT * FROM comunidade")
    comunidades = cursor.fetchall()

    return render_template('gerenciamento.html', profissoes=profissoes, profissionais=profissionais, comunidades=comunidades)

@app.route('/adicionar/<tabela>', methods=['POST'])
def adicionar(tabela):
    cursor = mysql.connection.cursor()

    if tabela == 'profissao':
        nome = request.form['nome']
        cursor.execute("INSERT INTO profissao (nome) VALUES (%s)", [nome])
    
    elif tabela == 'profissional':
        nome = request.form['nome']
        endereco = request.form['endereco']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        descricao = request.form['descricao']
        cursor.execute(
            "INSERT INTO profissional (nome, endereco, complemento, bairro, cidade, estado, descricao) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            [nome, endereco, complemento, bairro, cidade, estado, descricao]
        )
    
    elif tabela == 'comunidade':
        nome = request.form['nome']
        descricao = request.form['descricao']
        whatsapp = request.form['whatsapp']
        cursor.execute(
            "INSERT INTO comunidade (nome, descricao, whatsapp) VALUES (%s, %s, %s)",
            [nome, descricao, whatsapp]
        )
    
    mysql.connection.commit()
    return redirect(url_for('gerenciamento'))

@app.route('/alterar/profissional/<int:id>', methods=['GET', 'POST'])
def alterar_profissional(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Atualizar os dados do profissional
        nome = request.form['nome']
        endereco = request.form['endereco']
        complemento = request.form['complemento']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        descricao = request.form['descricao']

        cursor.execute("""
            UPDATE profissional
            SET Nome = %s, Endereco = %s, Complemento = %s, Bairro = %s, Cidade = %s, Estado = %s, Descricao = %s
            WHERE Id = %s
        """, (nome, endereco, complemento, bairro, cidade, estado, descricao, id))
        mysql.connection.commit()

        flash('Profissional atualizado com sucesso!', 'success')
        return redirect(url_for('gerenciamento'))

    # Carregar os dados do profissional para edição
    cursor.execute("SELECT * FROM profissional WHERE Id = %s", [id])
    profissional = cursor.fetchone()
    return render_template('alterar_profissional.html', profissional=profissional)



@app.route('/excluir/<tabela>/<int:id>', methods=['GET'])
def excluir(tabela, id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM {tabela} WHERE Id = %s", [id])
    mysql.connection.commit()
    return redirect(url_for('gerenciamento'))

if __name__ == '__main__':
    app.run(debug=True)
