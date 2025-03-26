import os
import logging
from scenedetect import open_video, SceneManager, ContentDetector, split_video_ffmpeg
from scenedetect.frame_timecode import FrameTimecode
import subprocess

# logging config
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Parámetros
carpeta_videos = r'./input'  # Input folder containing videos
min_duracion = 1.0  # Min clip duration in seconds
max_duracion = 2.99  # Max clip duration in seconds
directorio_salida = r'./output'  # Output folder for clips

logging.debug(f'Input Video Folder: {carpeta_videos}')
logging.debug(f'Output Video Folder: {directorio_salida}')

# Create the output directory if it does not exist
os.makedirs(directorio_salida, exist_ok=True)

# Function to process a single video
def procesar_video(ruta_video):
    logging.info(f'Processing {ruta_video}...')
    video = open_video(ruta_video)
    fps = video.frame_rate

    # Create scene manager and add content detector
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())

    # Detect scenes
    scene_manager.detect_scenes(video)
    escenas = scene_manager.get_scene_list()

    # Filter and adjust scenes
    escenas_filtradas = []
    for inicio, fin in escenas:
        duracion = (fin - inicio).get_seconds()
        if duracion < min_duracion:
            continue
        elif duracion > max_duracion:
            # Split the scene into maximum duration clips
            num_clips = int(duracion // max_duracion)
            for i in range(num_clips):
                clip_inicio = inicio + FrameTimecode(int(i * max_duracion * fps), fps)
                clip_fin = clip_inicio + FrameTimecode(int(max_duracion * fps), fps)
                escenas_filtradas.append((clip_inicio, clip_fin))
            # Add remaining part if longer than minimum duration
            resto = duracion % max_duracion
            if resto >= min_duracion:
                clip_inicio = inicio + FrameTimecode(int(num_clips * max_duracion * fps), fps)
                clip_fin = fin
                escenas_filtradas.append((clip_inicio, clip_fin))
        else:
            escenas_filtradas.append((inicio, fin))

    # Split video into filtered scenes
    nombre_video = os.path.splitext(os.path.basename(ruta_video))[0]
    directorio_video = os.path.join(directorio_salida, nombre_video)
    os.makedirs(directorio_video, exist_ok=True)
    split_video_ffmpeg(ruta_video, escenas_filtradas, output_dir=directorio_video)

    # Remove audio from generated clips
    for clip in os.listdir(directorio_video):
        if clip.endswith('.mp4'):
            ruta_clip = os.path.join(directorio_video, clip)
            ruta_clip_sin_audio = os.path.join(directorio_video, f'silent_{clip}')
            comando_ffmpeg = f'ffmpeg -i "{ruta_clip}" -an "{ruta_clip_sin_audio}"'
            subprocess.run(comando_ffmpeg, shell=True)
            os.remove(ruta_clip)
            os.rename(ruta_clip_sin_audio, ruta_clip)

    logging.info(f'Finished processing {ruta_video}.')

# Process all .mp4 files in the input folder
for archivo in os.listdir(carpeta_videos):
    if archivo.endswith('.mp4'):
        ruta_completa = os.path.join(carpeta_videos, archivo)
        logging.debug(f'Procesando archivo: {ruta_completa}')
        procesar_video(ruta_completa)