import enum
import streamlit as st
from gensim.models import KeyedVectors
from sklearn.decomposition import PCA
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.manifold import TSNE
from random import sample

wv = KeyedVectors.load("cbow_kv_pubmed_covid_7000.kv")


def sampled_words(sample_size=10):
    sampled = sample(list(wv.index_to_key), sample_size)
    return sampled


def run():
    st.title("Visualize Word2Vec")

    word = st.text_input(label="Test Word", value="Tests")
    topn = st.slider("Top N", 5, 25)

    if not word or word == "":
        st.write("No word received")
        return
    
    try:
        results = wv.most_similar(word, topn=topn)
    
    except KeyError:
        st.write("Word not found")
        return

    sim_words = [w for w, _ in results]
    sim_words.append(word)
    sim_vecs = wv[sim_words]

    pretty = [" ".join(w.split("_")) for w in sim_words]

    pca2 = PCA(n_components=2)
    pca30 = PCA(n_components=30)
    projected = pca2.fit_transform(sim_vecs)
    
    # sampled random words in vocab and use TSNE to see grouping
    num_words_to_sample = 5
    tsne2 = TSNE(n_components=2, perplexity=45, n_iter=500, early_exaggeration=16)
    sampled = sampled_words(num_words_to_sample)
    sampled.append(word)
    
    pretty_tsne = [" ".join(w.split("_")) for w in sampled]
    tsne_word_list = []
    
    for word in sampled:
        results = wv.most_similar(word, topn=100)
        sim_words = [w for w, _ in results]
        tsne_word_list.extend(sim_words)

    tsne_word_list.extend(sampled)
    tsne_wvs = wv[tsne_word_list]
    
    tsne2_projected = pca30.fit_transform(tsne_wvs)
    tsne2_projected = tsne2.fit_transform(tsne2_projected)
    
    projected_colors = np.zeros((projected.shape[0]))
    projected_colors[-1] = 1.
    
    colors_tsne2 = np.zeros((tsne2_projected.shape[0]))
    
    for idx, _ in enumerate(sampled):
        idx += 1
        color = idx*int(100/len(sampled))
        colors_tsne2[idx*100:(idx+1)*100] = color
    
    
    #tsne_all_vocab = np.load("tnse_transform.npy")
    
    fig, ax = plt.subplots(1,2, figsize=(5, 3))
    ax[0].scatter(x=tsne2_projected[:, 0], y=tsne2_projected[:, 1], s=1, c=colors_tsne2, cmap='tab10')
    ax[1].scatter(x=projected[:, 0], y=projected[:, 1], s=3, c=projected_colors)
    
    ax[0].tick_params(axis='x', labelsize=5)
    ax[0].tick_params(axis='y', labelsize=5)

    ax[1].tick_params(axis='x', labelsize=5)
    ax[1].tick_params(axis='y', labelsize=5)

        
    for i, w in enumerate(pretty):
        ax[1].annotate(w, xy=(projected[i, 0], projected[i, 1]), fontsize=5)
    
    for i, w in enumerate(pretty_tsne):
        len_words = len(tsne_word_list)
        index = len_words - len(pretty_tsne) + i
        coord = (tsne2_projected[index, 0], tsne2_projected[index, 1])
        ax[0].annotate(w, xy=coord, fontsize=5)
    
    st.pyplot(fig)

if __name__ == "__main__":
    run()