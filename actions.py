from copy import Error
from utils import extract_embeddings, get_cosine_simlarity, tensor_to_numpy, numpy_to_pickle, pickle_to_numpy, numpy_to_tensor
from crud import create_group, create_individual, read_group
from config import INFERENCE_THRESHOLD


def enroll(input_filepath, group_id='rev-speaker'):
    try:
        create_group(group_id)
        embeddings = extract_embeddings(input_filepath)
        embeddings = tensor_to_numpy(embeddings)
        create_individual(numpy_to_pickle(embeddings))
        return True
    except Exception as e:
        print(e)
        return False
    except Error as e:
        print(e)
        return False


def infer(input_filepath, group_id='rev-speaker'):
    embd1 = extract_embeddings(input_filepath)
    group = read_group(group_id)
    if group == None:
        return False, None
    for ind in group.individuals:
        embd2 = numpy_to_tensor(pickle_to_numpy(ind.embeddings))
        score = get_cosine_simlarity(embd1, embd2)
        print(f"SCORE: {score}")
        if score > INFERENCE_THRESHOLD:
            return True, ind.id
    return False, None
