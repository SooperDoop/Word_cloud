# main.py
from flask import Flask, request, render_template
from os import path
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
import pathlib
import os



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['image']
    
    text = request.form['words']
    
    f = os.path.join(file.filename)
    file.save(f)
    if pathlib.Path(r'static/img/chrt.jpeg').exists():
        os.remove(r'static/img/chrt.jpeg')
    
    
    alice_mask = np.array(Image.open(path.join(file.filename)))
    comment_words = ''
    stopwords = set(STOPWORDS) 
      
    # iterate through the csv file 
    for val in text.split(): 
        tokens = val.split() 
          
        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 
              
        for words in tokens: 
          comment_words = comment_words + words + ' '
      
      
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', mask=alice_mask,
                    stopwords = stopwords, 
                min_font_size = 10,).generate(comment_words) 
      
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.savefig('static/img/chrt.jpeg')
    
    
    
    
    
    return render_template('index.html', img = 'static/img/chrt.jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
