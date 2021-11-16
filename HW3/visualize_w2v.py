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
from operator import add, sub

wv = KeyedVectors.load("skip_model_cord19_covid_55k.kv")


def sampled_words(sample_size=10):
    sampled = sample(list(wv.index_to_key), sample_size)
    return sampled

def word_operation(words_to_workon, op):

    if op is add:
        op_str = " + "
    else:
        op_str = " - "

    words_for_op = []
    for w in words_to_workon:
        words_for_op.append(wv.get_vector(w, norm=True))

    diff = op(words_for_op[0], words_for_op[1])
    results = wv.similar_by_vector(diff)
    results = [w[0].replace("_", " ") for w in results[2:14]]
    results = "** " + ", ".join(results) + " **"
    st.subheader("{} {} {} = ".format(words_to_workon[0],
                                      op_str,
                                      words_to_workon[1]))

    st.write(results)


def run():

    size_of_vocab = len(list(wv.index_to_key))
    size_of_dim = wv.vector_size

    st.title("Visualize Word2Vec")

    st.header("Word Vector Embedding Statics")
    st.write("Numover of Vocab: {:,}".format(size_of_vocab))
    st.write("Dimensions: {}".format(size_of_dim))
    st.write("Size of Corpus: ~550K")

    st.header("Story 1: Try Some Word Operations")

    words_to_workon = ['COVID', 'virus']
    word_operation(words_to_workon, op=add)
    
    more_words1 = ['indoor', 'PPE']
    word_operation(more_words1, op=add)

    more_words5 = ['Indian', 'vaccine']
    word_operation(more_words5, op=add)

    more_words2 = ['work', 'disease']
    word_operation(more_words2, op=sub)

    more_words3 = ['doctor', 'surgeon']
    word_operation(more_words3, op=sub)

    result1 = wv.most_similar(positive=['man', 'nurse'], 
                              negative=['woman'], topn=1)[0][0].replace("_", " ")

    result2 = wv.most_similar(positive=['woman', 'doctor'],
                              negative=['man'], topn=1)[0][0]
    
    result3 = wv.most_similar(positive=['Moderna', "Pfizer"],
                              negative=['vaccine'], topn=1)[0][0]

    result4 = wv.most_similar(positive=["Alpha", "USA"],
                              negative='England', topn=4)

    result4 = ", ".join([w[0] for w in result4])
    #result4 = [", ".join(w for w in result4)]

    st.subheader("Nurse - Woman + Man = {}".format(result1.capitalize()))
    st.subheader("Doctor - Man + Woman = {}".format(result2.capitalize()))
    st.subheader("Moderna - vaccine + Pfizer = {}".format(result3.capitalize()))
    st.subheader("Alpha - England + USA = {}".format(result4))


    st.header("Story 2: Opposite Meaning do not equal to further distance:")
    
    word1 = st.text_input(label="Test Word 1 ", value="death")
    word2 = st.text_input(label="Test Word 2", value="alive")
    topn = st.slider("Top N", 5, 25)

    if not word1 or word1 == "":
        st.write("No word received")
        return
    
    try:
        results1 = wv.most_similar(word1, topn=topn)
    except KeyError:
        st.write("Word not in trained vocab")
        return

    sim_words_1 = [w for w, _ in results1]
    sim_words_1.append(word1)
    sim_vecs_1 = wv[sim_words_1]

    pretty = [" ".join(w.split("_")) for w in sim_words_1]

    pca2 = PCA(n_components=2)
    pca30 = PCA(n_components=30)
    projected = pca2.fit_transform(sim_vecs_1)
    
    # get topn word grouping for word1 and word2
    
    tsne2 = TSNE(n_components=2, perplexity=45, init="pca", 
                 n_iter=500, early_exaggeration=16, learning_rate='auto')

    tsne_word_list = []
    num_of_topn = 200

    try:
        for w in [word1, word2]:
            sim_words = wv.most_similar(w, topn=200)
            sim_words = [each for each, _ in sim_words]
            tsne_word_list.extend(sim_words)

            tsne_word_list.extend([word1, word2])
            tsne_wvs = wv[tsne_word_list]

    except KeyError:
        st.write("Word not in trained vocab!")
        return

    
    tsne2_projected = pca30.fit_transform(tsne_wvs)
    tsne2_projected = tsne2.fit_transform(tsne2_projected)
    
    projected_colors = np.zeros((projected.shape[0]))
    projected_colors[-1] = 1.
    
    colors_tsne2 = np.zeros((tsne2_projected.shape[0]))
    
    for idx, _ in enumerate([word1, word2]):
        idx += 1
        color = idx*int(num_of_topn/4)
        colors_tsne2[idx*num_of_topn:(idx+1)*num_of_topn] = color
    
    colors_tsne2[-1] = 100.
    colors_tsne2[-2] = 200.
    
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
    
    for i, w in enumerate([word1, word2]):
        len_words = len(tsne_word_list)
        index = len_words - 2 + i
        coord = (tsne2_projected[index, 0], tsne2_projected[index, 1])
        ax[0].annotate(w, xy=coord, fontsize=5)
    
    st.pyplot(fig)

if __name__ == "__main__":
    run()