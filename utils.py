from crud import read_profile
import ffmpeg
from torchaudio import load
from torch import from_numpy
from torch.nn import CosineSimilarity
from os import system, path
from pickle import loads
from scipy.io.wavfile import read, write
from numpy import hstack
import asyncio
from time import time
from models import EMBEDDINGS, PROFILE_ID

ALLOWED_EXTENSIONS = [".wav"]


def clean_dirs(*dirs):
    for dir in dirs:
        system(f"rm -rf {dir}/* &")


def make_dirs(*dirs):
    for dir in dirs:
        system(f"mkdir -p {dir} &")


async def extract_embeddings(filepath, classifier):
    print(f"2.1.1.1 {round(time() * 1000)}")
    signal, fs = load(filepath)
    print(f"2.1.1.2 {round(time() * 1000)}")
    embd = classifier.encode_batch(signal)
    print(f"2.1.1.3 {round(time() * 1000)}")
    return embd


# ensure same codecs


async def wav_audio_len_seconds(filepath):
    fs, data = read(filepath)
    return data.size / fs


async def concat_audio(base_file, new_file):
    base_fs, base_data = read(base_file)
    new_fs, new_data = read(new_file)
    if base_fs != new_fs:
        return 0
    base_data = hstack((base_data, new_data))
    write(base_file, base_fs, base_data)
    return base_data.size / base_fs


def tensor_to_numpy(embeddings):
    return embeddings.numpy()


def numpy_to_pickle(embeddings):
    return embeddings.dumps()


def pickle_to_numpy(pickle_dump):
    return loads(pickle_dump)


def numpy_to_tensor(numpy_array):
    return from_numpy(numpy_array)


def validate_extension(input_filepath):
    for ext in ALLOWED_EXTENSIONS:
        if input_filepath.endswith(ext):
            return True
    return False


# to compare two embeddings call the function as get_cosine_similarity(embd1, embd2)


async def audio_to_embeddings_pickle(filepath, classifier):
    return extract_embeddings(filepath, classifier)


def pickle_embeddings_to_tensor(pkl):
    return from_numpy(loads(pkl))


async def get_cosine_simlarity(*args, **kwargs):
    scorer = CosineSimilarity(dim=-1)
    return scorer(*args, **kwargs).item()


def convert_to_wav(input_filepath, output_filepath, **kwargs):
    try:
        (
            ffmpeg.input(input_filepath, **kwargs)
            .output(output_filepath, format="wav", acodec="pcm_s16le", ac=1, ar=16000)
            .overwrite_output()
            .run()
        )
        return True

    except Exception as e:
        print(e)
        return False


async def get_profile_scores(embeddings_idty, profile):
    print(f"2.4.1 {round(time() * 1000)}")
    embeddings_enr = pickle_embeddings_to_tensor(profile.get(EMBEDDINGS))
    score = await get_cosine_simlarity(embeddings_enr, embeddings_idty)
    print(f"2.4.2 {round(time() * 1000)}")
    return score, profile.get(PROFILE_ID)


async def identify_profile_list(audio_file, profile_id_list, classifier):
    print(f"2.1.1 {round(time() * 1000)}")
    embeddings_idty_task = asyncio.create_task(
        extract_embeddings(audio_file, classifier)
    )
    print(f"2.1.2 {round(time() * 1000)}")
    profiles_task = asyncio.create_task(read_profile(profile_id_list=profile_id_list))

    max_score, max_score_prof_id = 0, ""
    tasks = []
    embeddings_idty = await embeddings_idty_task
    print(f"2.1.3 {round(time() * 1000)}")
    # profiles = await profiles_task
    profiles = await profiles_task
    print(f"2.1.4 {round(time() * 1000)}")
    for prof in profiles:
        tasks.append(asyncio.create_task(get_profile_scores(embeddings_idty, prof)))
    print(f"2.1.5 {round(time() * 1000)}")
    results = await asyncio.gather(*tasks)
    for score, prof_id in results:
        if score > max_score:
            max_score = score
            max_score_prof_id = prof_id
    print(f"2.1.6 {round(time() * 1000)}")
    return max_score, max_score_prof_id


if __name__ == "__main__":
    print(
        extract_embeddings(
            path.join(path.dirname(__file__), "validated_wav_files/00000076.wav")
        )
    )
