from utils import (
    extract_embeddings,
    identify_profile_list,
    numpy_to_pickle,
    tensor_to_numpy,
)
from config import (
    S3_FOLDER_ACTIVE,
    S3_FOLDER_DELETED,
    UPLOAD_FOLDER,
    INFERENCE_THRESHOLD,
)
from flask import request, jsonify
from werkzeug.utils import secure_filename
import asyncio
from speechbrain.pretrained import EncoderClassifier
from status_codes import *
from uuid import uuid4
from utils import (
    concat_audio,
    convert_to_wav,
    validate_extension,
    wav_audio_len_seconds,
    clean_dirs,
    make_dirs,
)
from crud import create_profile, read_profile, update_profile, delete_profile
from models import app, ENROLLED_SECONDS, ENROLLMENT_COUNT, PROFILE_ID, PROFILE_ID_LIST
from s3_bucket_utils import bucket_copy, bucket_upl_dwl

# from apscheduler.schedulers.background import BackgroundScheduler
from time import time
from os import getcwd

# def connector():
#     Profile.query.exists()

print(getcwd())

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(connector, 'interval', seconds=2)
# sched.start()

make_dirs(S3_FOLDER_ACTIVE, UPLOAD_FOLDER, S3_FOLDER_DELETED)
classifier = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb")


async def new_enroll(output_filepath):
    profile_id = str(uuid4())
    bucket_upload_task = asyncio.create_task(
        bucket_upl_dwl.upload_file(
            output_filepath, f"{S3_FOLDER_ACTIVE}/{profile_id}.wav"
        )
    )

    audio_seconds_task = asyncio.create_task(wav_audio_len_seconds(output_filepath))

    embeddings_task = asyncio.create_task(
        extract_embeddings(output_filepath, classifier)
    )

    embeddings = await embeddings_task
    embeddings = numpy_to_pickle(tensor_to_numpy(embeddings))
    # if (await bucket_upload_task):
    #     return jsonify(response_obj)
    seconds = await audio_seconds_task
    create_profile_task = asyncio.create_task(
        create_profile(profile_id, seconds, embeddings)
    )
    await bucket_upload_task
    await create_profile_task
    return profile_id, 1, seconds


async def re_enroll(output_filepath, profile_id):
    bucket_download_task = asyncio.create_task(
        bucket_upl_dwl.download_file(
            f"{S3_FOLDER_ACTIVE}/{profile_id}.wav",
            f"{S3_FOLDER_ACTIVE}/{profile_id}.wav",
        )
    )

    read_profile_task = asyncio.create_task(read_profile(profile_id=profile_id))

    await bucket_download_task
    concat_audio_task = asyncio.create_task(
        concat_audio(output_filepath, f"{S3_FOLDER_ACTIVE}/{profile_id}.wav")
    )

    seconds = await concat_audio_task

    bucket_upload_task = asyncio.create_task(
        bucket_upl_dwl.upload_file(
            output_filepath, f"{S3_FOLDER_ACTIVE}/{profile_id}.wav"
        )
    )

    await bucket_upload_task
    embeddings_task = asyncio.create_task(
        extract_embeddings(output_filepath, classifier)
    )

    embeddings = await embeddings_task
    embeddings = numpy_to_pickle(tensor_to_numpy(embeddings))
    profile = (await read_profile_task).next()
    enrollment_count = profile.get(ENROLLMENT_COUNT) + 1
    await update_profile(
        profile_id=profile_id,
        enrollment_count=enrollment_count,
        enrolled_seconds=seconds,
        embeddings=embeddings,
    )
    return profile_id, enrollment_count, seconds


async def identify_profiles(output_filepath, profile_id_list, classifier):
    print(f"2.1 {round(time() * 1000)}")
    score, score_profile_id = await identify_profile_list(
        output_filepath, profile_id_list, classifier
    )
    print(f"2.2 {round(time() * 1000)}")
    return score, score_profile_id


@app.route("/api/v1/enroll", methods=["POST"])
def enroll():
    try:
        profile_id = request.args.get(PROFILE_ID)

        uploaded_file = request.files.get("file")
        if uploaded_file.filename != "":
            uploaded_file.filename = secure_filename(uploaded_file.filename)
        else:
            if profile_id != None:
                return jsonify(
                    {
                        PROFILE_ID: profile_id,
                        "status_code": FILE_DATA_ERROR,
                        "message": "Filename not found",
                    }
                )
            else:
                return jsonify(
                    {
                        "status_code": FILE_DATA_ERROR,
                        "message": "Filename not found",
                    }
                )

        input_filepath = f"{UPLOAD_FOLDER}/{uploaded_file.filename}"
        if validate_extension(input_filepath):
            uploaded_file.save(input_filepath)
        else:
            if profile_id != None:
                return jsonify(
                    {
                        PROFILE_ID: profile_id,
                        "status_code": EXTENSION_MISMATCH_ERROR,
                        "message": "Extension mismatch error",
                    }
                )
            else:
                return jsonify(
                    {
                        "status_code": EXTENSION_MISMATCH_ERROR,
                        "message": "Extension mismatch error",
                    }
                )

        output_filepath = f"{UPLOAD_FOLDER}/out_{uploaded_file.filename}"
        if convert_to_wav(input_filepath, output_filepath):

            if profile_id == None:
                profile_id, enrollment_count, seconds = asyncio.run(
                    new_enroll(output_filepath)
                )
                if profile_id == None:
                    return jsonify(
                        {
                            PROFILE_ID: profile_id,
                            "status_code": ENROLLMENT_FAILURE,
                            "message": "Enrollment Failed",
                        }
                    )
                else:
                    return jsonify(
                        {
                            PROFILE_ID: profile_id,
                            ENROLLMENT_COUNT: enrollment_count,
                            ENROLLED_SECONDS: seconds,
                            "status_code": ENROLLMENT_SUCCESS,
                            "message": "Enrollment Successful",
                        }
                    )
            else:
                prof_id, enrollment_count, seconds = asyncio.run(
                    re_enroll(output_filepath, profile_id)
                )
                if prof_id == None:
                    return jsonify(
                        {
                            PROFILE_ID: profile_id,
                            "status_code": ENROLLMENT_FAILURE,
                            "message": "Enrollment Failed",
                        }
                    )
                else:
                    return jsonify(
                        {
                            PROFILE_ID: prof_id,
                            ENROLLMENT_COUNT: enrollment_count,
                            ENROLLED_SECONDS: seconds,
                            "status_code": ENROLLMENT_SUCCESS,
                            "message": "Enrollment Success",
                        }
                    )

        else:
            return jsonify(
                {
                    "status_code": FILE_DATA_ERROR,
                    "message": "File data error",
                }
            )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "message": "Unknown error. Contact developer",
                "status_code": UNKNOWN_ERROR,
            }
        )


@app.route("/api/v1/identify", methods=["POST"])
def identify():
    try:
        args = request.args.to_dict()
        args[PROFILE_ID_LIST] = args[PROFILE_ID_LIST].split(",")
        if args.get(PROFILE_ID_LIST) == "" or args.get(PROFILE_ID_LIST) == None:
            return jsonify(
                {
                    "message": "Unknown error. Contact developer",
                    "status_code": UNKNOWN_ERROR,
                }
            )
        uploaded_file = request.files.get("file")
        if uploaded_file.filename != "":
            uploaded_file.filename = secure_filename(uploaded_file.filename)
        else:
            return jsonify(
                {
                    "status_code": FILE_DATA_ERROR,
                    "message": "Filename not found",
                }
            )

        input_filepath = f"{UPLOAD_FOLDER}/{uploaded_file.filename}"
        if validate_extension(input_filepath):
            uploaded_file.save(input_filepath)
        else:
            return jsonify(
                {
                    "status_code": EXTENSION_MISMATCH_ERROR,
                    "message": "Extension mismatch error",
                }
            )

        output_filepath = f"{UPLOAD_FOLDER}/out_{uploaded_file.filename}"
        print(f"1. {round(time() * 1000)}")
        # print(input_filepath)
        # print(output_filepath)
        if convert_to_wav(input_filepath, output_filepath):
            print(f"2. {round(time() * 1000)}")
            score, score_profile_id = asyncio.run(
                identify_profiles(
                    output_filepath, args.get(PROFILE_ID_LIST), classifier
                )
            )
            print(f"3. {round(time() * 1000)}")
            if score > INFERENCE_THRESHOLD:
                return jsonify(
                    {
                        PROFILE_ID: score_profile_id,
                        "status_code": INFERENCE_SUCCESS,
                        "message": "Identification success",
                    }
                )
            else:
                return jsonify(
                    {
                        "status_code": INFERENCE_FAILURE,
                        "message": "Identification failed",
                    }
                )

        else:
            return jsonify(
                {
                    "status_code": FILE_DATA_ERROR,
                    "message": "File data error",
                }
            )
    except Exception as e:
        print(e)
        return jsonify(
            {
                "message": "Unknown error. Contact developer",
                "status_code": UNKNOWN_ERROR,
            }
        )


@app.route("/api/v1/delete", methods=["POST"])
def delete():
    try:
        profile_id = request.args.get(PROFILE_ID)
        if profile_id == None or profile_id == "":
            return jsonify(
                {"status_code": DELETE_FAILURE, "message": "failed to delete profile"}
            )
        bucket_copy.move_file(
            f"{S3_FOLDER_ACTIVE}/{profile_id}.wav",
            f"{S3_FOLDER_DELETED}/{profile_id}.wav",
        )
        if delete_profile(profile_id=profile_id) > 0:
            return jsonify(
                {
                    PROFILE_ID: profile_id,
                    "status_code": DELETE_SUCCESS,
                    "message": "Profile deleted successfully",
                }
            )
        else:
            return jsonify(
                {
                    PROFILE_ID: profile_id,
                    "status_code": DELETE_FAILURE,
                    "message": "failed to delete profile",
                }
            )
    except Exception as e:
        print(e)
        return jsonify(
            {"message": "Unknown error. Contact developer", "status_code": ""}
        )


@app.teardown_appcontext
def clean_up(error):
    clean_dirs(S3_FOLDER_ACTIVE, UPLOAD_FOLDER)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # app.run(port=5000)
    # app.run(ssl_context='adhoc')
