from pytube import YouTube
from pytube import Playlist
import concurrent.futures
import re
import os 

data = {"lista" : "",
        "caracteres_no_permitidos" : r'[\/:*?"<>|]',}

def descargar_video(url, carpeta, format : str ="mp3"):
    """Descarga un video de youtube através de una url\n
    Formatos posibles: mp3 o mp4"""

    if os.path.exists(carpeta):
        data["lista"] = os.listdir(carpeta)
    else:
        os.mkdir(carpeta)
        data["lista"] = os.listdir(carpeta)
    video = YouTube(url)
    nombre = re.sub(data["caracteres_no_permitidos"], '_', video.title)
    ruta = os.path.join(carpeta, nombre + '.' + format)
    duracion = video.length
    data["duracion"].append(duracion)
    if not ruta in data["lista"]:
        if format == "mp3":
            video = video.streams.get_audio_only().download(filename=ruta, timeout=10)
        elif format == "mp4":
            video = video.streams.get_highest_resolution().download(filename=ruta, timeout=10)
        else:
            print("Error: Formato incorrecto\nDisponibles: mp3, mp4")

def descargar_lista_urls(lista_videos : list, carpeta, format : str = "mp3"):
    """Formatos posibles: mp3 o mp4"""
    if os.path.exists(carpeta):
        data["lista"] = os.listdir(carpeta)
    else:
        os.mkdir(carpeta)
        data["lista"] = os.listdir(carpeta)

    total = len(lista_videos)
    count = 0

    if format in ["mp3", "mp4"]:
        print("Descargando ...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            videos = []
            for video in lista_videos:
                videos.append(executor.submit(descargar_video, video, carpeta, format))

            for n in concurrent.futures.as_completed(videos):
                count += 1
                print(f'{count}/{total}')
    else:
        print("Error: Formato incorrecto\nDisponibles: mp3, mp4")
        return "Format error "

def descargar_playlist(playlist_url : str, carpeta, format : str = "mp3"):
    """Formatos posibles: mp3 o mp4"""
    if os.path.exists(carpeta):
        data["lista"] = os.listdir(carpeta)
    else:
        os.mkdir(carpeta)
        data["lista"] = os.listdir(carpeta)

    playlist = Playlist(playlist_url)
    total = len(playlist.video_urls)
    count = 0
    if format in ["mp3", "mp4"]:
        print("Descargando ...")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            videos = []
            for video in playlist.video_urls:
                videos.append(executor.submit(descargar_video, video, carpeta, format))

            for n in concurrent.futures.as_completed(videos):
                count += 1
                print(f'{count}/{total}')
    else:
        print("Error: Formato incorrecto\nDisponibles: mp3, mp4")
        return "Format error "
