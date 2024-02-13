import json
import torch
from tqdm import tqdm
from datasets import load_dataset
from joblib import Parallel, delayed 
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

STARTING_INDEX   = 50000
ENDING_INDEX     = 51000
CHUNKS           = 100
JOBS             = 5
PINECONE_INDEX   = "sandbox"
PINECONE_API_KEY = "78ac95ee-f064-481d-b5bb-f53c679762c1"
PINECONE_CHUNK   = 25

res             = []
dataset         = []
deduped_dataset = []
vectors         = []

def to_native_float(_list):
    return [a.item() for a in _list]

def chunker_list(seq, size):
    return (seq[i::size] for i in range(size))

def dedupe(dataset):
    deduped_dataset = []
    for index in range(len(dataset['questions'])):
        if dataset["is_duplicate"][i] == True:
            deduped_dataset.append(dataset['questions'][index]['text'][0])
        else:
            deduped_dataset.extend(dataset['questions'][index]['text'])
    return deduped_dataset

def get_device():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if device != 'cuda':
        print('Sorry no cuda.')
    return cuda


dataset = load_dataset('quora', split=f'train[{STARTING_INDEX}:{ENDING_INDEX}]')


chunked_dataset = [c for c in chunker_list(dataset, CHUNKS)]
deduped_result = Parallel(
    n_jobs=JOBS
)(
    delayed(dedupe)(x) for x in chunked_dataset
)

deduped_result = []
for _list in result:
    deduped_result.extend(_list)
deduped_result = list(set(deduped_result))


print(len(deduped_result))


print("####### LOADING LLM #########")
model = SentenceTransformer('all-MiniLM-L6-v2', device=get_device())


print("####### CONNECTING TO VECTOR STORE (pinecone) #########")
pc             = Pinecone(api_key=PINECONE_API_KEY)
pinecone_index = pc.Index(PINECONE_INDEX)



print("####### INDEXING DOCS #########")
for batch_id, batch in enumerate(chunker_list(deduped_result, len(deduped_result)//PINECONE_CHUNK)):
    document_ids = [f'batch{batch_id}_{i}' for i in range(len(batch))] 
    encodings    = model.encode(batch)
    metadata     = [{"text": doc} for doc in batch]

    for i in range(len(document_ids)):
        vectors.append({
            "id"       : document_ids[i],
            "values"   : encodings[i],
            "metadata" : metadata[i]
        })

    index.upsert(
        vectors=vectors,
        namespace= "ns1"
    )


print("####### QUERYING NOW .... #########")
response = index.query(
    namespace="ns1",
    vector= to_native_float(model.encode('where do I go for food in India ?')),
    top_k=5,
    include_values=True,
    include_metadata=True
)


