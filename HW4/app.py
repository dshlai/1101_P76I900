from pynndescent.distances import dot
import streamlit as st
import textacy
import textacy
import textacy.representations.vectorizers as vectorizers
import numpy as np
import umap
import umap.plot
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances, manhattan_distances

st.title("TF-IDF Document Similarity")

# Select Corpus to compare
options = st.multiselect("What Corpus you want to compare?", default=["TV", "Food"],
                         options=["TV", "Food", "Health", "Politics"])

selection_a = st.selectbox(label="Select a Document from {}".format(options[0]), options=[1,2,3,4])
selection_b = st.selectbox(label="Select a Document from {}".format(options[1]), options=[1,2,3,4])

dist_metirc = st.selectbox(label="Select a Distance Metrics", options=["L1", "L2", "Cosine"])

corpus_4cls = textacy.Corpus.load("en_core_web_trf", "../../models/P76I900/HW4/wikinews_4cls_corpus.bin.gz")

tv_class = np.zeros([200]).astype(int)
food_class = np.ones([141]).astype(int)
health_class = np.ones([200]).astype(int) * 2
poli_class = np.ones([200]).astype(int) * 3

total_class = np.concatenate([tv_class, food_class, health_class, poli_class])

corpus_tv = corpus_4cls[0:200]
corpus_food = corpus_4cls[200:200+141]
corpus_health = corpus_4cls[200+141:200+141+200]
corpus_poli = corpus_4cls[200+141+200:-1]

corpus_dict = {"TV": corpus_tv, "Food": corpus_food, 
               "Health": corpus_health, "Politics": corpus_poli}

label_dict = {"TV": tv_class, "Food": food_class, "Health": health_class, "Politics": poli_class}

metrics_dict = {"L1": manhattan_distances, "Cosine": cosine_distances, "L2": euclidean_distances}

if len(options) < 2:
    st.write("Cannot compare less than 2 Corpus")
else:
    compare_list = []
    labels = []

    for opt in options:
        compare_list.extend(corpus_dict[opt])
        labels.append(label_dict[opt])

    labels = np.concatenate(labels)

    vectorizer = vectorizers.Vectorizer(tf_type='linear', idf_type='smooth')

    tokenized = ((term.lemma_ for term in textacy.extract.terms(doc, ngs=1, ents=True, ncs=True, dedupe=True)) for doc in compare_list)
    dot_cls = vectorizer.fit_transform(tokenized)

    st.write(corpus_dict[options[0]][selection_a])
    st.write(corpus_dict[options[1]][selection_b])

    dm = metrics_dict[dist_metirc]

    a = dot_cls[selection_a-1].toarray()
    b = dot_cls[selection_b-1].toarray()

    dist = dm(a,b)[0][0]
    st.subheader("Distance between documents is {}".format(dist))

    #mapped = umap.UMAP(n_components=2, metric='hellinger', random_state=42).fit_transform(dot_cls)
    #umap.plot.points(mapper, labels=labels)

    #plt.scatter(mapped[:, 0], mapped[:, 1], c=labels, cmap='tab20', s=2)
    #plt.show()