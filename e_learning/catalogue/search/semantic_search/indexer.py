from requests.auth import HTTPBasicAuth
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import requests
import cohere
import json
import time

CSV_FILE_NAME  = '/Users/utsavtiwary/Downloads/course_catalog_embedded_small.csv'
COHERE_KEY     = "MQoohnbLFGgS8ZhjFXJyyO15QSeLobPcQHuRtsCc"
ES_URL         = "http://localhost:9200"
ES_USERNAME    = "elastic"
ES_PASSWORD    = "pzYymOMRt=-pdvfwbj*d"
INDEX          = "course_catalog"
N_CLUSTERS     = 10
EMBEDDING_SIZE = 1024
INDEX_PARAMS   = {
    "mappings": {
        "_source": {"enabled": True },
        "properties": {
            "year":    {"type": "integer"},
            "term":    {"type": "keyword"},
            "subject": {"type": "keyword"},
            "number":  {"type": "integer"},
            "name":    {"type": "text", "analyzer": "standard"},
            "description": {"type": "text", "analyzer": "standard"},
            "embedding":   {
                "type": "dense_vector",
                "dims": EMBEDDING_SIZE,
                "index": True,
                "similarity": "cosine"
            }
        }
    }
}
def prompt(msg, wait=2):
    print(msg)
    print("\n")
    time.sleep(wait)

def visualize_vectors(course_catalog: pd.DataFrame, clusters=N_CLUSTERS):
    vectors = []
    for em in course_catalog.itertuples():
        vectors.append([float(i) for i in em.course_name_vectors.replace("[", "").replace("]", "").split(",")])

    pca = PCA(n_components=2)
    pca.fit(vectors)
    reduced_vectors = pd.DataFrame(pca.fit_transform(vectors, 2).tolist())

    x, y   = [d[0] for d in reduced_vectors.values], [d[1] for d in reduced_vectors.values]
    kmeans = KMeans(n_clusters=clusters)
    labels = kmeans.fit_predict(reduced_vectors)

    plt.scatter(x, y, c=labels, cmap='jet')
    # for i, label in enumerate(labels):
    #     plt.annotate(label, pd.DataFrame(reduced_vectors).iloc[i, :])
    plt.show()

def create_index(index_params=INDEX_PARAMS):
    try:
        response = requests.put(
            f"{ES_URL}/{INDEX}",
            data=json.dumps(index_params),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            print(f"Failed to create index {str(INDEX)} :: {response.status_code} :: {response.text}")

    except Exception as e:
        raise Exception(f"Failed to create index {str(INDEX)} :: {str(e)}")

def create_document(doc):
    try:
        response = requests.post(
            f"{ES_URL}/{INDEX}/_doc/",
            data=json.dumps(doc),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            print(f"Failed to create new document in {INDEX} :: {doc['name']} :: {response.status_code} {response.text}")
            return None

        return response.json()["_id"]

    except Exception as e:
        raise Exception(f"Failed to create new document in {INDEX} :: {doc['name']} :: {str(e)}")

def search_document(search_text):

    def generate_cohere_embeddings(text):
        co        = cohere.Client(COHERE_KEY)
        embedding = co.embed([text], 'embed-english-light-v2.0') ## Dim : COHERE_BATCH_SIZE x 1024

        return embedding.embeddings[0]

    try:
        query_vector = generate_cohere_embeddings(search_text)
        response     = requests.post(
            f"{ES_URL}/{INDEX}/_search/",
            data=json.dumps({
              "knn": {
                "field": "embedding",
                "query_vector": query_vector,
                "k": 10,
                "num_candidates": 100
              },
              "fields": [ "name", "description" ]
            }),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            print(f"Failed to search document in {INDEX} :: {search_text} :: {response.status_code} :: {response.text}")
            return None

        return [doc["_source"] for doc in response.json()['hits']['hits']]

    except Exception as e:
        raise Exception(f"Failed to search document in {INDEX} :: {search_text} :: {str(e)}")


######
prompt(f"Loading file with embeddings ...")
######
course_catalog = pd.read_csv(CSV_FILE_NAME)
doc_list       = []
for doc in course_catalog.itertuples():
    doc_list.append({
        "year":        doc.Year,
        "term":        doc.Term ,
        "subject":     doc.Subject,
        "number":      doc.Number,
        "name":        doc.Name,
        "description": doc.Description or "",
        "embedding":   [float(i) for i in doc.course_name_vectors.replace("[", "").replace("]", "").split(",")]
    })

######
prompt(f"Creating ES Index and indexing docs ...")
######
create_index()
for doc in doc_list:
    if create_document(doc) is None:
        print("ERROR STOP")
        exit(0)

######
prompt(f"Viasualizing models ...")
######
visualize_vectors(course_catalog)

######
prompt(f"Search ...")
######
visualize_vectors(course_catalog)


# requests.post
# {
#     "size": 10,
#     "query": {
#         "script_score": {
#             "query": {"match_all": {}},
#             "script": {
#                 "source": "cosineSimilarity(params.query_vector, doc['title_vector']) + 1.0",
#                 "params": {"query_vector": query_vector}
#             }
#         }
#     },
#     "_source": {"includes": ["Name", "Description"]}
# }
