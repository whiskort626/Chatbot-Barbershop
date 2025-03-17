from flask import Flask, jsonify, request

app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    idWa=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['id']
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['timestamp']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    #SI HAY UN MENSAJE  
    if mensaje is not None:
      from rivescript import RiveScript
      #INICIAMOS EL CHATBOT
      bot = RiveScript()
      #CARGAMOS EL ARCHIVO DE RESPUESTAS
      bot.load_file("restaurante.rive")
      #ORDENAMOS LAS RESPUESTAS
      bot.sort_replies()
      #OBTENEMOS LA RESPUESTA DEL CHATBOT
      respuesta = bot.reply("localuser", mensaje)
      #CAMBIAMOS LOS \n POR \n
      respuesta = respuesta.replace("\\n", "\n")
      #ELIMINAMOS LAS COMILLAS
      respuesta = respuesta.replace("\\", "")
      #ESCRIBIMOS LA RESPUESTA EN EL ARCHIVO TEXTO
      f = open("texto.txt", "w")
      f.write(respuesta)
      #CERRAMOS EL ARCHIVO
      f.close()
      #RETORNAMOS EL STATUS EN UN JSON
    return jsonify({"status": "success"}, 200)

#INICIAMSO FLASK
if __name__ == "__main__":
  app.run(debug=True)