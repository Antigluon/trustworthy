import nltk
import parser
import keras
import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding
import tensorflow as tf
from tensorflow.keras.preprocessing.text import one_hot
nltk.download('punkt')

model = tf.keras.models.load_model('data/lstm_model.h5')
model._make_predict_function()

# prediciting if the current article is reliable or not
def reliable(file):
    with open(file, 'r') as file:
        text = file.read().replace('\n', ' ')
    
    text = nltk.tokenize.sent_tokenize(text)
    
    text=[token.lower() for token in text]
    
    onehot_enc=[one_hot(words,10000) for words in text]
    sen_len=300
    embedded_doc=pad_sequences(onehot_enc, padding='pre', maxlen=sen_len)
    text_final=np.array(embedded_doc)
    
    pred = model.predict(text_final)
    
    pred_df = pd.DataFrame(pred)
    text_df = pd.DataFrame(text)
    result_df = pd.concat([pred_df, text_df], axis=1)
    
    pred_df.columns = ["predictions"]
    
    result_df.columns = ["predictions", "Sentence"]
    
    print(result_df.loc[result_df['predictions'] <= 0.7])
    
    fakeres_df = result_df.loc[result_df['predictions'] <= 0.7]
    fake_df = fakeres_df["Sentence"]
    
    return fake_df
    
    # print(pred_df["predictions"].mean())
    
reliable("/kaggle/input/cnn-article/message-2.txt")
    
