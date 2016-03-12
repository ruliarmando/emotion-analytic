import twitter
from flask import Blueprint, render_template, request, current_app as app
from sklearn.externals import joblib


analytic = Blueprint('analytic', __name__)


@analytic.route('/')
def home():
    return 'sentiment analytic app'

    
@analytic.route('/search', methods=['GET', 'POST'])
def search():
    count = 100
    statuses = []
    q = ''
    
    if request.method == 'POST':
        q = request.form['q']
        
        auth = twitter.oauth.OAuth(
            app.config['ACCESS_TOKEN'],
            app.config['ACCESS_TOKEN_SECRET'],
            app.config['CONSUMER_KEY'],
            app.config['CONSUMER_SECRET']
        )
        
        twitter_api = twitter.Twitter(auth=auth)
    
        search_results = twitter_api.search.tweets(q=q, count=count)
    
        statuses = search_results['statuses']
    
    return render_template('search.html', statuses=statuses, q=q)
    
    
@analytic.route('/classify', methods=['POST'])
def classify():
    sentence = request.form['sentence']
    sentence = sentence.translate(dict((ord(char), None) for char in "1234567890'"))
    vect = joblib.load('E:/PROGRAMMING/python/projects/sentiment/my_app/analytic/vect.pkl')
    tf = joblib.load('E:/PROGRAMMING/python/projects/sentiment/my_app/analytic/tf.pkl')
    fs = joblib.load('E:/PROGRAMMING/python/projects/sentiment/my_app/analytic/fs.pkl')
    svm = joblib.load('E:/PROGRAMMING/python/projects/sentiment/my_app/analytic/clf.pkl')
    bow = vect.transform([sentence])
    X = tf.transform(bow)
    X = fs.transform(X)
    predict = svm.predict(X)
    return predict[0]