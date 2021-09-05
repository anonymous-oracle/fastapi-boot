from time import time
from models import PROFILE_ID_LIST, db
from models import PROFILE_ID, ID, ENROLLED_SECONDS, ENROLLMENT_COUNT, EMBEDDINGS

# CREATE


async def create_profile(profile_id, enrolled_seconds, embeddings):
    try:
        db.Profile.insert_one(
            {
                PROFILE_ID: profile_id,
                ENROLLED_SECONDS: enrolled_seconds,
                ENROLLMENT_COUNT: 1,
                EMBEDDINGS: embeddings,
            }
        )
        return True
    except Exception as e:
        print(e)
        return False


# READ
# kwargs = {
#     "profile_id": None,
#     "profile_id_list": None
# }


async def read_profile(**kwargs):
    print(f"2.1.2.1 {round(time() * 1000)}")
    var = kwargs.get(PROFILE_ID_LIST)
    if var != None:
        print(f"2.1.2.2 {round(time() * 1000)}")
        return db.Profile.find({PROFILE_ID: {"$in": var}})
    var = kwargs.get(PROFILE_ID)
    if var != None:
        return db.Profile.find({PROFILE_ID: var})
    var = kwargs.get("_id")
    if var != None:
        return db.Profile.find({"_id": var})
    return None


# UPDATE
# kwargs = {"profile_id": None,
#           "enrolled_seconds": None,
#           "enrollment_count": None,
#           "embeddings ": None
#           }


async def update_profile(**kwargs):
    profile_id = kwargs.get(PROFILE_ID)
    enrolled_seconds = kwargs.get(ENROLLED_SECONDS)
    enrolled_count = kwargs.get(ENROLLMENT_COUNT)
    embeddings = kwargs.get(EMBEDDINGS)
    try:
        result = db.Profile.update_one(
            {PROFILE_ID: profile_id},
            {
                "$set": {
                    PROFILE_ID: profile_id,
                    ENROLLED_SECONDS: enrolled_seconds,
                    ENROLLMENT_COUNT: enrolled_count,
                    EMBEDDINGS: embeddings,
                }
            },
        )
        return result.matched_count
    except Exception as e:
        print(e)
        return 0


# DELETE

# kwargs = {
#     "id": None,
#     "profile_id": None
# }


def delete_profile(**kwargs):
    try:
        var = kwargs.get(PROFILE_ID)
        if var != None:
            res = db.Profile.delete_one({PROFILE_ID: var})
            return res.deleted_count
        var = kwargs.get("_id")
        if var != None:
            res = db.Profile.delete_one({"_id": var})
            return res.deleted_count
    except Exception as e:
        print(e)
        return 0
