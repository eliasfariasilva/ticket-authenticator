from flask import Blueprint, request, jsonify

from .models import QRCode

from . import db

views = Blueprint('views', __name__)

@views.route('/criar_ingresso', methods = ['POST'])
def create_ticket():
    code = request.form.get('code')

    newQRcode = QRCode(code = code)

    db.session.add(newQRcode)
    
    db.session.commit()


    return {'mensagem': 'Ingresso Criado com Sucesso!'}


@views.route('/validar_ingresso/<string:qr_code>', methods=['GET'])
def validar_ingresso(qr_code):
    try:
        # Buscar o QR code no banco de dados
        qr_code_obj = QRCode.query.filter_by(code=qr_code).first()

        # Verificar se o QR code existe e se já foi utilizado
        if qr_code_obj:
            if qr_code_obj.used:
                resposta = {'status': 'Invalido', 'mensagem': 'Ingresso já utilizado'}
            else:
                # Marcar o QR code como utilizado no banco de dados
                qr_code_obj.used = True
                db.session.commit()
                resposta = {'status': 'Aprovado', 'mensagem': 'Ingresso válido'}
        else:
            resposta = {'status': 'Invalido', 'mensagem': 'Ingresso inválido'}

    except KeyError:
        resposta = {'status': 'Erro', 'mensagem': 'QR code ausente na solicitação'}

    return jsonify(resposta)






