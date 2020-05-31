import nltk
import parser
nltk.download('punkt')

model = tf.keras.models.load_model('data/lstm_model.h5')

# prediciting if the current article is reliable or not
def reliable(text):
    
    text = nltk.tokenize.sent_tokenize(text)
    
    text=[token.lower() for token in text]
    
    onehot_enc=[one_hot(words,100000) for words in text]
    sen_len=300
    embedded_doc=pad_sequences(onehot_enc, padding='pre', maxlen=sen_len)
    text_final=np.array(embedded_doc)
    
    pred = model.predict_classes(text_final)
    
    pred_df = pd.DataFrame(pred)
    text_df = pd.DataFrame(text)
    result_df = pd.concat([pred_df, text_df], axis=1)
    
    print(result_df)
    
article = parser.Strip("https://www.foxnews.com/us/minnesota-national-guard-full-mobilization-george-floyd")
if article.is_success():
    reliable(article.raw_text())
