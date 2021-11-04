import streamlit as st
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import pandas as pd
import altair as alt
from matplotlib import pyplot as plt
import numpy as np

wv = KeyedVectors.load("cbow_kv_pubmed_covid_7000.kv")


def run():
    st.title("Visualize Word2Vec")

    word = st.text_input(label="Test Word", value="Tests")
    topn = st.slider("Top N", 5, 50)

    
    results = wv.most_similar(word, topn=topn)

    sim_words = [w for w, _ in results]
    sim_words.append(word)
    vecs = wv[sim_words]

    pretty = [" ".join(w.split("_")) for w in sim_words]

    pca = PCA(n_components=2)
    projected = pca.fit_transform(vecs)

    colors = np.zeros((projected.shape[0], 1))
    colors[-1,0] = 1.

    fig, ax = plt.subplots()
    ax.scatter(projected[:, 0], projected[:,1], c=colors)

    for i, w in enumerate(pretty):
        ax.annotate(w, xy=(projected[i, 0], projected[i, 1]))
    
    st.pyplot(fig)

if __name__ == "__main__":
    run()