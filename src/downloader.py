import yt_dlp


def baixar_video(url):
    opcoes = {
        "outtmpl": "downloads/mp4/%(title)s.%(ext)s",
        "format": "bv*+ba/b",
        "merge_output_format": "mp4",
    }

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    url = input("Cole a URL do YouTube: ")

    try:
        baixar_video(url)
        print("\nDownload concluído!")

    except Exception as erro:
        print("\nErro durante o download:")
        print(erro)