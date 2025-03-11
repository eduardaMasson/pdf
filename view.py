from flask import Flask, send_file
from main import app, con
from fpdf import FPDF


import jwt
app.config.from_pyfile('config.py')


@app.route('/usuario/relatorio', methods=['GET'])
def usuario_relatorio():
    cursor = None
    try:
        cursor = con.cursor()
        cursor.execute("SELECT id_usuario, nome, e_mail, senha FROM usuario")
        usuarios = cursor.fetchall()
    finally:
        if cursor:
            cursor.close()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Relatório de Usuários", ln=True, align='C')

    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)

    pdf.set_font("Arial", size=12)
    for usuario in usuarios:
        pdf.cell(200, 10, f"ID: {usuario[0]} - Nome: {usuario[1]} - E-mail: {usuario[2]} - Senha: {usuario[3]}", ln=True)

    contador_usuarios = len(usuarios)
    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, f"Total de usuários cadastrados: {contador_usuarios}", ln=True, align='C')

    pdf_path = "relatorio_usuarios.pdf"
    pdf.output(pdf_path)
    return send_file(pdf_path, as_attachment=True, mimetype='application/pdf')























@app.route('/imagem', methods=['POST'])
def imagem():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'mensagem': 'Token de autenticação necessário'}), 401

    token = remover_bearer(token)
    try:
        payload = jwt.decode(token, senha_secreta, algorithms=['HS256'])
        id_usuario = payload['id_usuario']
    except jwt.ExpiredSignatureError:
        return jsonify({'mensagem': 'Token expirado'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'mensagem': 'Token inválido'}), 401

    # Recebendo os dados do formulário (não JSON)
    nome = request.form.get('nome')
    e_mail = request.form.get('e_mail')
    senha = request.form.get('senha')
    imagem = request.files.get('imagem')  # Arquivo enviado

    cursor = con.cursor()

    # Verifica se já existe
    cursor.execute("SELECT 1 FROM usuario WHERE nome = ?", (nome,))
    if cursor.fetchone():
        cursor.close()
        return jsonify({"error": "Usuário já cadastrado"}), 400

    # Insere o novo livro e retorna o ID gerado
    cursor.execute(
        "INSERT INTO usuario (nome, e_mail, senha) VALUES (?, ?, ?) RETURNING id_usuario",
        (nome, e_mail, senha)
    )
    usuario_id = cursor.fetchone()[0]
    con.commit()

    # Salvar a imagem se for enviada
    imagem_path = None
    if imagem:
        nome_imagem = f"{usuario_id}.jpeg"  # Define o nome fixo com .jpeg
        pasta_destino = os.path.join(app.config['UPLOAD_FOLDER'], "Livros")
        os.makedirs(pasta_destino, exist_ok=True)
        imagem_path = os.path.join(pasta_destino, nome_imagem)
        imagem.save(imagem_path)


    cursor.close()

    return jsonify({
        'message': "Usuário cadastrado com sucesso!",
        'usuario': {
            'id': usuario_id,
            'nome': nome,
            'e_mail': e_mail,
            'senha': senha,
            'imagem_path': imagem_path
        }
    }), 201













// começo do view


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])








