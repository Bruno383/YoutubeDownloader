from flask import Flask, render_template, request, jsonify, send_file
import os
import urllib.parse
import yt_dlp

from src.config import MP4_DIR, MP3_DIR


app = Flask(__name__)


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ============================================================
# ENTREGA O ARQUIVO PARA O CELULAR / COMPUTADOR
# ============================================================

@app.route("/arquivo")
def arquivo():

    formato = request.args.get("formato", "MP4").upper()
    nome = request.args.get("nome", "")

    nome = urllib.parse.unquote(nome)

    # Segurança: impede acesso a arquivos fora da pasta de downloads
    nome = os.path.basename(nome)

    if formato == "MP4":
        pasta = MP4_DIR
        mimetype = "video/mp4"

    elif formato == "MP3":
        pasta = MP3_DIR
        mimetype = "audio/mpeg"

    else:
        return "Formato inválido.", 400

    caminho = os.path.join(pasta, nome)

    if not os.path.isfile(caminho):
        return "Arquivo não encontrado.", 404

    return send_file(
        caminho,
        mimetype=mimetype,
        as_attachment=True,
        download_name=nome
    )


# ============================================================
# DOWNLOAD DO YOUTUBE
# ============================================================

@app.route("/download", methods=["POST"])
def download():

    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({
            "sucesso": False,
            "erro": "Dados inválidos."
        }), 400

    url = dados.get("url", "").strip()
    formato = dados.get("formato", "MP4").upper()
    qualidade = dados.get("qualidade", "Melhor disponível")

    if not url:
        return jsonify({
            "sucesso": False,
            "erro": "Cole uma URL do YouTube."
        }), 400

    # ========================================================
    # MP4
    # ========================================================

    if formato == "MP4":

        pasta = MP4_DIR

        if qualidade == "Melhor disponível":

            formato_video = (
                "bv*[vcodec^=avc1][acodec^=mp4a]/"
                "bv*[vcodec^=avc1]+ba[acodec^=mp4a]/"
                "bv*+ba/b"
            )

        else:

            try:
                altura = int(qualidade.replace("p", ""))

                if altura <= 0:
                    raise ValueError

            except (ValueError, AttributeError):
                return jsonify({
                    "sucesso": False,
                    "erro": "Qualidade de vídeo inválida."
                }), 400

            formato_video = (
                f"bv*[height<={altura}]"
                f"[vcodec^=avc1]+"
                f"ba[acodec^=mp4a]/"
                f"bv*[height<={altura}]+"
                f"ba/b[height<={altura}]"
            )

        opcoes = {
            "outtmpl": os.path.join(
                pasta,
                "%(title)s.%(ext)s"
            ),

            "format": formato_video,
            "merge_output_format": "mp4",
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,

            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4"
                }
            ]
        }

    # ========================================================
    # MP3
    # ========================================================

    elif formato == "MP3":

        pasta = MP3_DIR

        qualidade_mp3 = qualidade.replace(" kbps", "")

        if qualidade_mp3 not in ["320", "192", "128"]:
            qualidade_mp3 = "192"

        opcoes = {
            "outtmpl": os.path.join(
                pasta,
                "%(title)s.%(ext)s"
            ),

            "format": "bestaudio/best",

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": qualidade_mp3
                }
            ],

            "noplaylist": True,
            "quiet": True,
            "no_warnings": True
        }

    else:
        return jsonify({
            "sucesso": False,
            "erro": "Formato inválido."
        }), 400

    # ========================================================
    # EXECUTAR DOWNLOAD
    # ========================================================

    try:

        os.makedirs(pasta, exist_ok=True)

        arquivos_antes = set(os.listdir(pasta))

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(
                url,
                download=True
            )

        arquivos_depois = set(os.listdir(pasta))

        novos_arquivos = arquivos_depois - arquivos_antes

        # ----------------------------------------------------
        # PROCURAR ARQUIVO FINAL
        # ----------------------------------------------------

        if formato == "MP4":

            candidatos = [
                nome
                for nome in arquivos_depois
                if nome.lower().endswith(".mp4")
            ]

        else:

            candidatos = [
                nome
                for nome in arquivos_depois
                if nome.lower().endswith(".mp3")
            ]

        candidatos_novos = [
            nome
            for nome in candidatos
            if nome in novos_arquivos
        ]

        if candidatos_novos:

            nome_arquivo = candidatos_novos[0]

        elif candidatos:

            nome_arquivo = max(
                candidatos,
                key=lambda nome: os.path.getmtime(
                    os.path.join(pasta, nome)
                )
            )

        else:
            return jsonify({
                "sucesso": False,
                "erro": (
                    "O download terminou, mas o arquivo final "
                    "não foi encontrado."
                )
            }), 500

        # ====================================================
        # CONFIRMAR ARQUIVO
        # ====================================================

        caminho_final = os.path.join(
            pasta,
            nome_arquivo
        )

        if not os.path.isfile(caminho_final):
            return jsonify({
                "sucesso": False,
                "erro": "Arquivo final não encontrado."
            }), 500

        # ====================================================
        # URL DE DOWNLOAD
        # ====================================================

        url_download = (
            "/arquivo?formato="
            + urllib.parse.quote(formato)
            + "&nome="
            + urllib.parse.quote(nome_arquivo)
        )

        # ====================================================
        # RESPOSTA DE SUCESSO
        # ====================================================

        return jsonify({
            "sucesso": True,
            "mensagem": "Download concluído!",
            "arquivo": nome_arquivo,
            "url_download": url_download
        })

    except Exception as erro:

        mensagem = str(erro)
        mensagem_minuscula = mensagem.lower()

        # ----------------------------------------------------
        # BLOQUEIO / AUTENTICAÇÃO DO YOUTUBE
        # ----------------------------------------------------

        if (
            "sign in to confirm" in mensagem_minuscula
            or "confirm you're not a bot" in mensagem_minuscula
            or "confirm you’re not a bot" in mensagem_minuscula
            or "cookies" in mensagem_minuscula
            and "authentication" in mensagem_minuscula
        ):

            mensagem_usuario = (
                "O YouTube bloqueou esta solicitação e exige "
                "uma verificação de acesso. Tente novamente "
                "mais tarde ou utilize um vídeo acessível "
                "sem autenticação."
            )

            status_http = 502

        else:

            mensagem_usuario = (
                "Não foi possível concluir o download. "
                "Verifique o link e tente novamente."
            )

            status_http = 500

        # Registra o detalhe técnico nos logs do servidor
        app.logger.error(
            "Falha no download: %s",
            mensagem
        )

        return jsonify({
            "sucesso": False,
            "erro": mensagem_usuario
        }), status_http


# ============================================================
# INICIAR SERVIDOR LOCAL
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
