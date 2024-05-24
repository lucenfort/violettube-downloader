import os
import flet as ft
from pytube import YouTube, Playlist
from moviepy.editor import AudioFileClip

def main(page: ft.Page):
    # Configurações iniciais da página
    page.title = "VioletTube Downloader"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#8A2BE2"  # Violeta sólido

    # Função para criar diretórios se não existirem
    def create_directories():
        os.makedirs("Audio", exist_ok=True)
        os.makedirs("Video", exist_ok=True)

    create_directories()  # Criar diretórios no início

    # Função para atualizar a barra de progresso
    def progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = bytes_downloaded / total_size
        download_progress.value = progress
        page.update()

    # Função para download de vídeo
    def download_video(url, resolution):
        try:
            yt = YouTube(url, on_progress_callback=progress_callback)
            ys = yt.streams.filter(res=resolution).first()
            if ys:
                video_name.value = yt.title
                ys.download(output_path="Video")
                status.value = f"Download do vídeo em {resolution} concluído!"
            else:
                status.value = "Erro: Resolução não disponível para este vídeo."
        except Exception as e:
            status.value = f"Erro ao baixar vídeo: {e}"
        finally:
            download_progress.value = 0
            page.update()

    # Função para converter áudio
    def convert_audio(input_path, output_path, audio_format):
        audio_clip = AudioFileClip(input_path)
        audio_clip.write_audiofile(output_path, codec='pcm_s16le' if audio_format == 'wav' else None)

    # Função para download de áudio
    def download_audio(url, audio_format):
        try:
            yt = YouTube(url, on_progress_callback=progress_callback)
            ys = yt.streams.filter(only_audio=True).first()
            if ys:
                video_name.value = yt.title
                temp_file = ys.download(output_path="Audio")
                if audio_format != "mp4":
                    base, ext = os.path.splitext(temp_file)
                    new_file = base + f".{audio_format}"
                    convert_audio(temp_file, new_file, audio_format)
                    os.remove(temp_file)
                status.value = f"Download do áudio em {audio_format} concluído!"
            else:
                status.value = "Erro: Formato de áudio não disponível para este vídeo."
        except Exception as e:
            status.value = f"Erro ao baixar áudio: {e}"
        finally:
            download_progress.value = 0
            page.update()

    # Função para download de playlist
    def download_playlist(url, is_video, option):
        try:
            pl = Playlist(url)
            total_videos = len(pl.video_urls)
            current_video = 0
            for video_url in pl.video_urls:
                current_video += 1
                try:
                    yt = YouTube(video_url, on_progress_callback=progress_callback)
                    if is_video:
                        ys = yt.streams.filter(res=option).first()
                    else:
                        ys = yt.streams.filter(only_audio=True).first()
                    if ys:
                        video_name.value = yt.title
                        temp_file = ys.download(output_path="Video" if is_video else "Audio")
                        if not is_video and option != "mp4":
                            base, ext = os.path.splitext(temp_file)
                            new_file = base + f".{option}"
                            convert_audio(temp_file, new_file, option)
                            os.remove(temp_file)
                        status.value = f"Baixando {'vídeo' if is_video else 'áudio'} {current_video} de {total_videos}..."
                    else:
                        status.value = f"Erro: {'Resolução' if is_video else 'Formato de áudio'} não disponível para o vídeo {current_video}."
                except Exception as e:
                    status.value = f"Erro ao baixar {'vídeo' if is_video else 'áudio'} {current_video}: {e}"
                finally:
                    page.update()
            status.value = f"Download da playlist de {'vídeos' if is_video else 'áudios'} em {option} concluído!"
        except Exception as e:
            status.value = f"Erro ao processar playlist: {e}"
        finally:
            download_progress.value = 0
            page.update()

    # Definindo os componentes da interface
    title = ft.Text("VioletTube Downloader", size=40, color=ft.colors.WHITE)
    url_input = ft.TextField(label="URL do YouTube", width=500)

    download_type = ft.Dropdown(
        label="Tipo de Download",
        options=[
            ft.dropdown.Option("Áudio"),
            ft.dropdown.Option("Vídeo")
        ]
    )

    resolution_options = ft.Dropdown(
        label="Resolução (Vídeo)",
        options=[
            ft.dropdown.Option("144p"),
            ft.dropdown.Option("360p"),
            ft.dropdown.Option("720p"),
            ft.dropdown.Option("1080p"),
            ft.dropdown.Option("4k")
        ],
        visible=False
    )

    audio_format_options = ft.Dropdown(
        label="Formato (Áudio)",
        options=[
            ft.dropdown.Option("mp3"),
            ft.dropdown.Option("wav")
        ],
        visible=False
    )

    playlist_toggle = ft.Checkbox(label="Baixar Playlist")
    status = ft.Text("", color="#39FF14", weight=ft.FontWeight.BOLD, size=16)  # Verde radioativo
    video_name = ft.Text("", color="#39FF14", weight=ft.FontWeight.BOLD, size=16)  # Verde radioativo
    download_progress = ft.ProgressBar(width=500, height=20, color=ft.colors.BLUE, value=0)

    # Função para atualizar visibilidade das opções
    def update_options(e):
        if download_type.value == "Áudio":
            resolution_options.visible = False
            audio_format_options.visible = True
        else:
            resolution_options.visible = True
            audio_format_options.visible = False
        page.update()

    download_type.on_change = update_options

    # Função para iniciar download
    def start_download(e):
        url = url_input.value
        download_progress.value = 0
        video_name.value = ""
        if playlist_toggle.value:
            if download_type.value == "Áudio":
                download_playlist(url, False, audio_format_options.value)
            else:
                download_playlist(url, True, resolution_options.value)
        else:
            if download_type.value == "Áudio":
                download_audio(url, audio_format_options.value)
            else:
                download_video(url, resolution_options.value)

    download_button = ft.ElevatedButton(text="Baixar", on_click=start_download)

    # Adicionando componentes à página e centralizando
    page.add(
        ft.Column(
            [
                title,
                url_input,
                download_type,
                resolution_options,
                audio_format_options,
                playlist_toggle,
                download_button,
                download_progress,
                video_name,
                status
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=main)
