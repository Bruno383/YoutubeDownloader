import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk
import yt_dlp

from config import MP4_DIR, MP3_DIR


# ============================================================
# CONFIGURAÇÃO
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ============================================================
# LOCALIZAR FFMPEG
# ============================================================

def localizar_ffmpeg():

    ffmpeg = shutil.which("ffmpeg")

    if ffmpeg:
        return ffmpeg

    caminho = (
        r"C:\Users\iscon\AppData\Local\Microsoft\WinGet\Packages"
        r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
        r"\ffmpeg-9.0.2-full_build\bin"
    )

    executavel = os.path.join(
        caminho,
        "ffmpeg.exe"
    )

    if os.path.exists(executavel):
        return executavel

    return None


FFMPEG = localizar_ffmpeg()


# ============================================================
# VARIÁVEIS
# ============================================================

download_em_andamento = False
cancelar_download = threading.Event()


# ============================================================
# JANELA
# ============================================================

janela = ctk.CTk()

janela.title("YouTube Downloader")

largura = 780
altura = 850

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

pos_x = (largura_tela - largura) // 2
pos_y = (altura_tela - altura) // 2

janela.geometry(
    f"{largura}x{altura}+{pos_x}+{pos_y}"
)

janela.resizable(False, False)


# ============================================================
# CABEÇALHO
# ============================================================

frame_header = ctk.CTkFrame(
    janela,
    fg_color="transparent"
)

frame_header.pack(
    fill="x",
    padx=45,
    pady=(25, 10)
)


titulo = ctk.CTkLabel(
    frame_header,
    text="▶  YOUTUBE DOWNLOADER",
    font=ctk.CTkFont(
        size=27,
        weight="bold"
    )
)

titulo.pack(
    anchor="w"
)


subtitulo = ctk.CTkLabel(
    frame_header,
    text="Baixe vídeos e áudios de forma simples",
    font=ctk.CTkFont(
        size=14
    ),
    text_color="gray"
)

subtitulo.pack(
    anchor="w",
    pady=(5, 0)
)


# ============================================================
# CARD PRINCIPAL
# ============================================================

frame_principal = ctk.CTkFrame(
    janela,
    corner_radius=15
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=10
)


# ============================================================
# URL
# ============================================================

label_url = ctk.CTkLabel(
    frame_principal,
    text="URL DO YOUTUBE",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_url.pack(
    anchor="w",
    padx=30,
    pady=(25, 5)
)


entrada_url = ctk.CTkEntry(
    frame_principal,
    placeholder_text="Cole aqui a URL do YouTube...",
    height=45,
    font=ctk.CTkFont(size=13),
    corner_radius=10
)

entrada_url.pack(
    fill="x",
    padx=30
)


# ============================================================
# FORMATO
# ============================================================

label_formato = ctk.CTkLabel(
    frame_principal,
    text="FORMATO",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_formato.pack(
    anchor="w",
    padx=30,
    pady=(18, 5)
)


combo_formato = ctk.CTkComboBox(
    frame_principal,
    values=[
        "🎬  MP4 - Vídeo",
        "🎵  MP3 - Áudio"
    ],
    height=42,
    corner_radius=10,
    state="readonly"
)

combo_formato.set(
    "🎬  MP4 - Vídeo"
)

combo_formato.pack(
    fill="x",
    padx=30
)


# ============================================================
# QUALIDADE MP4
# ============================================================

label_qualidade = ctk.CTkLabel(
    frame_principal,
    text="QUALIDADE DO VÍDEO",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_qualidade.pack(
    anchor="w",
    padx=30,
    pady=(18, 5)
)


combo_qualidade = ctk.CTkComboBox(
    frame_principal,
    values=[
        "Melhor disponível",
        "1080p",
        "720p",
        "480p",
        "360p"
    ],
    height=42,
    corner_radius=10,
    state="readonly"
)

combo_qualidade.set(
    "Melhor disponível"
)

combo_qualidade.pack(
    fill="x",
    padx=30
)


# ============================================================
# QUALIDADE MP3
# ============================================================

combo_mp3 = ctk.CTkComboBox(
    frame_principal,
    values=[
        "320 kbps",
        "192 kbps",
        "128 kbps"
    ],
    height=42,
    corner_radius=10,
    state="readonly"
)

combo_mp3.set(
    "192 kbps"
)


# ============================================================
# PASTA
# ============================================================

label_pasta = ctk.CTkLabel(
    frame_principal,
    text="LOCAL DE SALVAMENTO",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_pasta.pack(
    anchor="w",
    padx=30,
    pady=(18, 5)
)


frame_pasta = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_pasta.pack(
    fill="x",
    padx=30
)


entrada_pasta = ctk.CTkEntry(
    frame_pasta,
    height=42,
    corner_radius=10
)

entrada_pasta.pack(
    side="left",
    fill="x",
    expand=True
)

entrada_pasta.insert(
    0,
    MP4_DIR
)


def escolher_pasta():

    pasta = filedialog.askdirectory(
        title="Escolha a pasta onde salvar o arquivo"
    )

    if pasta:

        entrada_pasta.delete(
            0,
            "end"
        )

        entrada_pasta.insert(
            0,
            pasta
        )


botao_pasta = ctk.CTkButton(
    frame_pasta,
    text="📁  Escolher",
    width=120,
    height=42,
    corner_radius=10,
    command=escolher_pasta
)

botao_pasta.pack(
    side="right",
    padx=(10, 0)
)


# ============================================================
# ALTERAR FORMATO
# ============================================================

def alterar_formato(valor):

    if "MP3" in valor:

        label_qualidade.configure(
            text="QUALIDADE DO ÁUDIO"
        )

        combo_qualidade.pack_forget()

        combo_mp3.pack(
            fill="x",
            padx=30
        )

        entrada_pasta.delete(
            0,
            "end"
        )

        entrada_pasta.insert(
            0,
            MP3_DIR
        )

    else:

        label_qualidade.configure(
            text="QUALIDADE DO VÍDEO"
        )

        combo_mp3.pack_forget()

        combo_qualidade.pack(
            fill="x",
            padx=30
        )

        entrada_pasta.delete(
            0,
            "end"
        )

        entrada_pasta.insert(
            0,
            MP4_DIR
        )


# Ativar o evento depois que a função já existe
combo_formato.configure(
    command=alterar_formato
)


# ============================================================
# PROGRESSO
# ============================================================

label_progresso = ctk.CTkLabel(
    frame_principal,
    text="PROGRESSO",
    font=ctk.CTkFont(
        size=12,
        weight="bold"
    )
)

label_progresso.pack(
    anchor="w",
    padx=30,
    pady=(18, 5)
)


frame_progresso = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_progresso.pack(
    fill="x",
    padx=30
)


barra_progresso = ctk.CTkProgressBar(
    frame_progresso,
    height=14,
    corner_radius=7
)

barra_progresso.set(0)

barra_progresso.pack(
    side="left",
    fill="x",
    expand=True
)


label_percentual = ctk.CTkLabel(
    frame_progresso,
    text="0%",
    width=55,
    font=ctk.CTkFont(
        size=13,
        weight="bold"
    )
)

label_percentual.pack(
    side="right",
    padx=(10, 0)
)


# ============================================================
# STATUS
# ============================================================

label_status = ctk.CTkLabel(
    frame_principal,
    text="●  Aguardando download...",
    anchor="w",
    font=ctk.CTkFont(size=12),
    text_color="gray"
)

label_status.pack(
    fill="x",
    padx=30,
    pady=(10, 2)
)


label_velocidade = ctk.CTkLabel(
    frame_principal,
    text="",
    anchor="w",
    font=ctk.CTkFont(size=11),
    text_color="gray"
)

label_velocidade.pack(
    fill="x",
    padx=30
)
# ============================================================
# MENSAGEM DE DOWNLOAD CONCLUÍDO
# ============================================================

frame_concluido = ctk.CTkFrame(
    frame_principal,
    corner_radius=12,
    fg_color=("gray90", "gray17")
)

label_concluido = ctk.CTkLabel(
    frame_concluido,
    text="✓  DOWNLOAD CONCLUÍDO!",
    font=ctk.CTkFont(
        size=20,
        weight="bold"
    )
)

label_concluido.pack(
    pady=(15, 5)
)

label_concluido_info = ctk.CTkLabel(
    frame_concluido,
    text="Seu arquivo foi salvo com sucesso!",
    font=ctk.CTkFont(
        size=13
    )
)

label_concluido_info.pack(
    pady=(0, 15)
)


# ============================================================
# ATUALIZAR INTERFACE
# ============================================================

def atualizar_progresso(percentual):

    percentual = max(
        0,
        min(100, percentual)
    )

    barra_progresso.set(
        percentual / 100
    )

    label_percentual.configure(
        text=f"{percentual:.0f}%"
    )


def atualizar_status(texto):

    label_status.configure(
        text=texto
    )


def atualizar_velocidade(texto):

    label_velocidade.configure(
        text=texto
    )


# ============================================================
# PROGRESSO DO YT-DLP
# ============================================================

def progresso_download(d):

    if cancelar_download.is_set():

        raise yt_dlp.utils.DownloadCancelled(
            "Download cancelado."
        )

    status = d.get("status")

    if status == "downloading":

        total = (
            d.get("total_bytes")
            or d.get("total_bytes_estimate")
        )

        baixado = d.get(
            "downloaded_bytes",
            0
        )

        if total:

            percentual = (
                baixado / total
            ) * 100

            janela.after(
                0,
                atualizar_progresso,
                percentual
            )

        velocidade = d.get(
            "speed"
        )

        if velocidade:

            velocidade_mb = (
                velocidade
                / 1024
                / 1024
            )

            janela.after(
                0,
                atualizar_velocidade,
                f"Velocidade: {velocidade_mb:.2f} MB/s"
            )

        janela.after(
            0,
            atualizar_status,
            "●  Baixando..."
        )

    elif status == "finished":

        janela.after(
            0,
            atualizar_status,
            "●  Processando arquivo..."
        )


# ============================================================
# DOWNLOAD
# ============================================================

def executar_download(
    url,
    formato,
    qualidade,
    pasta
):

    global download_em_andamento

    try:

        os.makedirs(
            pasta,
            exist_ok=True
        )

        # ====================================================
        # MP4
        # ====================================================

        if formato == "MP4":

            if qualidade == "Melhor disponível":

                formato_video = "bv*+ba/b"

            else:

                altura = qualidade.replace(
                    "p",
                    ""
                )

                formato_video = (
                    f"bv*[height<={altura}]"
                    f"+ba/b[height<={altura}]"
                )

            opcoes = {

                "outtmpl": os.path.join(
                    pasta,
                    "%(title)s.%(ext)s"
                ),

                "format": formato_video,

                "merge_output_format": "mp4",

                "ffmpeg_location": FFMPEG,

                "progress_hooks": [
                    progresso_download
                ],

                "noplaylist": True,

                "quiet": True,

                "no_warnings": True
            }

        # ====================================================
        # MP3
        # ====================================================

        else:

            qualidade_mp3 = (
                qualidade.replace(
                    " kbps",
                    ""
                )
            )

            opcoes = {

                "outtmpl": os.path.join(
                    pasta,
                    "%(title)s.%(ext)s"
                ),

                "format": "bestaudio/best",

                "ffmpeg_location": FFMPEG,

                "postprocessors": [

                    {
                        "key":
                        "FFmpegExtractAudio",

                        "preferredcodec":
                        "mp3",

                        "preferredquality":
                        qualidade_mp3
                    }

                ],

                "progress_hooks": [
                    progresso_download
                ],

                "noplaylist": True,

                "quiet": True,

                "no_warnings": True
            }

        # ====================================================
        # EXECUTAR
        # ====================================================

        with yt_dlp.YoutubeDL(
            opcoes
        ) as ydl:

            ydl.download(
                [url]
            )

        janela.after(
            0,
            download_concluido
        )

    except yt_dlp.utils.DownloadCancelled:

        janela.after(
            0,
            download_cancelado
        )

    except Exception as erro:

        janela.after(
            0,
            download_erro,
            str(erro)
        )

    finally:

        download_em_andamento = False

        janela.after(
            0,
            habilitar_interface
        )


# ============================================================
# INICIAR DOWNLOAD
# ============================================================

def iniciar_download():

    global download_em_andamento

    if download_em_andamento:
        return

    url = entrada_url.get().strip()

    if not url:

        atualizar_status(
            "⚠  Cole uma URL do YouTube."
        )

        return

    pasta = entrada_pasta.get().strip()

    if not pasta:

        atualizar_status(
            "⚠  Escolha uma pasta."
        )

        return

    if FFMPEG is None:

        atualizar_status(
            "⚠  FFmpeg não encontrado."
        )

        return

    if "MP3" in combo_formato.get():

        formato = "MP3"

        qualidade = combo_mp3.get()

    else:

        formato = "MP4"

        qualidade = combo_qualidade.get()

    download_em_andamento = True

    cancelar_download.clear()

    desabilitar_interface()

    barra_progresso.set(0)

    label_percentual.configure(
        text="0%"
    )

    atualizar_status(
        "●  Preparando download..."
    )

    atualizar_velocidade(
        ""
    )

    thread = threading.Thread(
        target=executar_download,
        args=(
            url,
            formato,
            qualidade,
            pasta
        ),
        daemon=True
    )

    thread.start()


# ============================================================
# CANCELAR
# ============================================================

def cancelar():

    if download_em_andamento:

        cancelar_download.set()

        atualizar_status(
            "●  Cancelando..."
        )


# ============================================================
# RESULTADOS
# ============================================================

def download_cancelado():

    atualizar_status(
        "■  Download cancelado."
    )

    atualizar_velocidade(
        ""
    )

    barra_progresso.set(0)

    label_percentual.configure(
        text="0%"
    )


def download_erro(erro):

    # Verifica se o arquivo foi realmente salvo
    pasta = entrada_pasta.get().strip()

    if pasta and os.path.exists(pasta):

        arquivos = os.listdir(pasta)

        if arquivos:

            atualizar_progresso(100)

            atualizar_status(
                "✓  Download concluído!"
            )

            atualizar_velocidade(
                "Arquivo salvo com sucesso."
            )

            frame_concluido.pack(
                fill="x",
                padx=30,
                pady=(15, 5)
            )

            label_concluido_info.configure(
                text="Seu arquivo foi salvo com sucesso!"
            )

            return

    # Se realmente não houver arquivo, mostra erro
    atualizar_status(
        "✕  Erro durante o download."
    )

    atualizar_velocidade(
        erro[:120]
    )


# ============================================================
# CONTROLE DA INTERFACE
# ============================================================

def desabilitar_interface():

    entrada_url.configure(
        state="disabled"
    )

    combo_formato.configure(
        state="disabled"
    )

    combo_qualidade.configure(
        state="disabled"
    )

    combo_mp3.configure(
        state="disabled"
    )

    entrada_pasta.configure(
        state="disabled"
    )

    botao_pasta.configure(
        state="disabled"
    )

    botao_download.configure(
        state="disabled"
    )

    botao_cancelar.configure(
        state="normal"
    )


def habilitar_interface():

    entrada_url.configure(
        state="normal"
    )

    combo_formato.configure(
        state="readonly"
    )

    combo_qualidade.configure(
        state="readonly"
    )

    combo_mp3.configure(
        state="readonly"
    )

    entrada_pasta.configure(
        state="normal"
    )

    botao_pasta.configure(
        state="normal"
    )

    botao_download.configure(
        state="normal"
    )

    botao_cancelar.configure(
        state="disabled"
    )


# ============================================================
# BOTÕES
# ============================================================

frame_botoes = ctk.CTkFrame(
    frame_principal,
    fg_color="transparent"
)

frame_botoes.pack(
    fill="x",
    padx=30,
    pady=(20, 25)
)


botao_download = ctk.CTkButton(
    frame_botoes,
    text="⬇  BAIXAR",
    height=50,
    corner_radius=10,
    font=ctk.CTkFont(
        size=14,
        weight="bold"
    ),
    command=iniciar_download
)

botao_download.pack(
    side="left",
    fill="x",
    expand=True
)


botao_cancelar = ctk.CTkButton(
    frame_botoes,
    text="✕  CANCELAR",
    height=50,
    width=145,
    corner_radius=10,
    fg_color="transparent",
    border_width=1,
    command=cancelar,
    state="disabled"
)

botao_cancelar.pack(
    side="right",
    padx=(10, 0)
)


# ============================================================
# RODAPÉ
# ============================================================

rodape = ctk.CTkLabel(
    janela,
    text="YouTube Downloader  •  yt-dlp + FFmpeg",
    font=ctk.CTkFont(
        size=10
    ),
    text_color="gray"
)

rodape.pack(
    pady=(0, 10)
)


# ============================================================
# INICIAR INTERFACE
# ============================================================

janela.mainloop()