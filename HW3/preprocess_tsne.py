from gensim.models import KeyedVectors
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


wv = KeyedVectors.load("cbow_kv_pubmed_covid_7000.kv")

# get all vectors
all_vecs = []
for _, key in enumerate(list(wv.index_to_key)):
    all_vecs.append(wv[key])
    
all_vecs = np.stack(all_vecs, axis=0)

pca = PCA(n_components=30)
tnse = TSNE(n_components=2, perplexity=50, n_iter=500, n_jobs=-1)
pca_transformed = pca.fit_transform(all_vecs)
tnse_transformed = tnse.fit_transform(pca_transformed)

np.save("tnse_transform.npy", tnse_transformed)
