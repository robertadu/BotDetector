FROM python:3

RUN pip install requests
RUN pip install pydantic
RUN pip install numpy 
RUN pip install pandas 
RUN pip install textblob 
RUN pip install nltk 
RUN pip install scikit-learn 
RUN pip install pickle-mixin

# Download NLTK corpora required for TextBlob
RUN python -m nltk.downloader punkt averaged_perceptron_tagger wordnet brown vader_lexicon

#Important so we will have access to the run.sh file 
COPY . . 

CMD ["sh", "run.sh"]
