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