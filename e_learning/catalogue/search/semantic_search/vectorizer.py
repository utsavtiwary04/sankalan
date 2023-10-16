###

# import necessary tools
# setup index
# convert docs to vectors (generate embeddings)
# store vectors + docs in DB
# generate query vector (embedding)
# query and fetch best score

###


## incorporate feedback to improve models ?


###
import csv
import time
import cohere
import pandas as pd
from sklearn.decomposition import PCA

COHERE_KEY         = "MQoohnbLFGgS8ZhjFXJyyO15QSeLobPcQHuRtsCc"
COHERE_RATE_LIMIT  = 8 #seconds
COHERE_BATCH_SIZE  = 48
COURSE_CATALOG_URL = "https://waf.cs.illinois.edu/discovery/course-catalog.csv"
CSV_FILE_NAME      = '/Users/utsavtiwary/Downloads/course_catalog_embedded.csv'

def prompt(msg, wait=2):
	print(msg)
	print("\n")
	time.sleep(wait)

def generate_cohere_embeddings(batch):
	time.sleep(COHERE_RATE_LIMIT)
	co = cohere.Client(COHERE_KEY)
	batch_embeddings = co.embed(batch, 'embed-english-light-v2.0') ## Dim : COHERE_BATCH_SIZE x 1024

	return batch_embeddings.embeddings

######
prompt(f"Loading model ...")
######


######
prompt(f"Reading remote source file ...")
######

course_catalog = pd.read_csv(COURSE_CATALOG_URL).drop_duplicates(subset=['Name', 'Description'], keep='last')

######
prompt(f"Generating embeddings ...")
######

batches = []
batch   = []
vectors = []

for row in course_catalog.itertuples():
	batch.append(row.Name)

	if len(batch) == COHERE_BATCH_SIZE:
		vectors.extend([e for e in generate_cohere_embeddings(batch)])
		batch = []
		prompt(f"{len(vectors)} embeddings generated", 10)

if len(batch) > 0:
	vectors.extend([e for e in generate_cohere_embeddings(batch)])
	prompt(f"{len(vectors)} embeddings generated", 10)

######
prompt(f"{len(vectors)} embeddings generated !")
######

######
prompt(f"Running PCA for reducing dimensions ...")
######
# pca             = PCA(n_components=2)
# pca.fit(vectors)
# reduced_vectors = pca.fit_transform(vectors, 2).tolist()

######
prompt(f"Dumping to CSV file ..")
######

# course_catalog['course_name_vectors'] = reduced_vectors
course_catalog['course_name_vectors'] = vectors
course_catalog.to_csv(f'/Users/utsavtiwary/Downloads/course_catalog_embedded_{int(time.time())}.csv')

######
prompt(f"Done !")
######
