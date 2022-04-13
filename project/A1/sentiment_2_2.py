#!/usr/bin/env python
# coding: utf-8

# In[1]:


def read_files_token_pattern(tarfname,n):
    """Read the training and development data from the sentiment tar file.
    The returned object contains various fields that store sentiment data, such as:

    train_data,dev_data: array of documents (array of words)
    train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
    train_labels,dev_labels: the true string label for each document (same length as data)

    The data is also preprocessed for use with scikit-learn, as:

    count_vec: CountVectorizer used to process the data (for reapplication on new data)
    trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
    le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
    target_labels: List of labels (same order as used in le)
    trainy,devy: array of int labels, one for each document
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    trainname = "train.tsv"
    devname = "dev.tsv"
    for member in tar.getmembers():
        if 'train.tsv' in member.name:
            trainname = member.name
        elif 'dev.tsv' in member.name:
            devname = member.name
            
            
    class Data: pass
    sentiment = Data()
    print("-- train data")
    sentiment.train_data, sentiment.train_labels = read_tsv(tar,trainname)
    print(len(sentiment.train_data))

    print("-- dev data")
    sentiment.dev_data, sentiment.dev_labels = read_tsv(tar, devname)
    print(len(sentiment.dev_data))
    print("-- transforming data and labels")
    from sklearn.feature_extraction.text import TfidfVectorizer
    sentiment.tfidf_vect = TfidfVectorizer(token_pattern=r"(?u)\b[A-Za-z][A-Za-z]+\b", ngram_range=(1,n))
    sentiment.trainX = sentiment.tfidf_vect.fit_transform(sentiment.train_data)
    sentiment.devX = sentiment.tfidf_vect.transform(sentiment.dev_data)
    from sklearn import preprocessing
    sentiment.le = preprocessing.LabelEncoder()
    sentiment.le.fit(sentiment.train_labels)
    sentiment.target_labels = sentiment.le.classes_
    sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
    sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
    tar.close()
    return sentiment


# In[2]:


def read_files_stop_words(tarfname,n):
    """Read the training and development data from the sentiment tar file.
    The returned object contains various fields that store sentiment data, such as:

    train_data,dev_data: array of documents (array of words)
    train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
    train_labels,dev_labels: the true string label for each document (same length as data)

    The data is also preprocessed for use with scikit-learn, as:

    count_vec: CountVectorizer used to process the data (for reapplication on new data)
    trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
    le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
    target_labels: List of labels (same order as used in le)
    trainy,devy: array of int labels, one for each document
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    trainname = "train.tsv"
    devname = "dev.tsv"
    for member in tar.getmembers():
        if 'train.tsv' in member.name:
            trainname = member.name
        elif 'dev.tsv' in member.name:
            devname = member.name
            
            
    class Data: pass
    sentiment = Data()
    print("-- train data")
    sentiment.train_data, sentiment.train_labels = read_tsv(tar,trainname)
    print(len(sentiment.train_data))

    print("-- dev data")
    sentiment.dev_data, sentiment.dev_labels = read_tsv(tar, devname)
    print(len(sentiment.dev_data))
    print("-- transforming data and labels")
    from sklearn.feature_extraction.text import TfidfVectorizer
    stwlist = ["and","the","am","is","are","a","an"]
    sentiment.tfidf_vect = TfidfVectorizer(stop_words=stwlist, ngram_range=(1,n))
    sentiment.trainX = sentiment.tfidf_vect.fit_transform(sentiment.train_data)
    sentiment.devX = sentiment.tfidf_vect.transform(sentiment.dev_data)
    from sklearn import preprocessing
    sentiment.le = preprocessing.LabelEncoder()
    sentiment.le.fit(sentiment.train_labels)
    sentiment.target_labels = sentiment.le.classes_
    sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
    sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
    tar.close()
    return sentiment


# In[3]:


def read_files_token_pattern_stop_words(tarfname,n):
    """Read the training and development data from the sentiment tar file.
    The returned object contains various fields that store sentiment data, such as:

    train_data,dev_data: array of documents (array of words)
    train_fnames,dev_fnames: list of filenames of the doccuments (same length as data)
    train_labels,dev_labels: the true string label for each document (same length as data)

    The data is also preprocessed for use with scikit-learn, as:

    count_vec: CountVectorizer used to process the data (for reapplication on new data)
    trainX,devX: array of vectors representing Bags of Words, i.e. documents processed through the vectorizer
    le: LabelEncoder, i.e. a mapper from string labels to ints (stored for reapplication)
    target_labels: List of labels (same order as used in le)
    trainy,devy: array of int labels, one for each document
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    trainname = "train.tsv"
    devname = "dev.tsv"
    for member in tar.getmembers():
        if 'train.tsv' in member.name:
            trainname = member.name
        elif 'dev.tsv' in member.name:
            devname = member.name
            
            
    class Data: pass
    sentiment = Data()
    print("-- train data")
    sentiment.train_data, sentiment.train_labels = read_tsv(tar,trainname)
    print(len(sentiment.train_data))

    print("-- dev data")
    sentiment.dev_data, sentiment.dev_labels = read_tsv(tar, devname)
    print(len(sentiment.dev_data))
    print("-- transforming data and labels")
    from sklearn.feature_extraction.text import TfidfVectorizer
    stwlist = ["and","the","am","is","are","a","an"]
    sentiment.tfidf_vect = TfidfVectorizer(stop_words=stwlist, token_pattern=r"(?u)\b[A-Za-z][A-Za-z]+\b", ngram_range=(1,n))
    sentiment.trainX = sentiment.tfidf_vect.fit_transform(sentiment.train_data)
    sentiment.devX = sentiment.tfidf_vect.transform(sentiment.dev_data)
    from sklearn import preprocessing
    sentiment.le = preprocessing.LabelEncoder()
    sentiment.le.fit(sentiment.train_labels)
    sentiment.target_labels = sentiment.le.classes_
    sentiment.trainy = sentiment.le.transform(sentiment.train_labels)
    sentiment.devy = sentiment.le.transform(sentiment.dev_labels)
    tar.close()
    return sentiment


# In[4]:


def read_unlabeled(tarfname, sentiment):
    """Reads the unlabeled data.

    The returned object contains three fields that represent the unlabeled data.

    data: documents, represented as sequence of words
    fnames: list of filenames, one for each document
    X: bag of word vector for each document, using the sentiment.vectorizer
    """
    import tarfile
    tar = tarfile.open(tarfname, "r:gz")
    class Data: pass
    unlabeled = Data()
    unlabeled.data = []
    
    unlabeledname = "unlabeled.tsv"
    for member in tar.getmembers():
        if 'unlabeled.tsv' in member.name:
            unlabeledname = member.name
            
    print(unlabeledname)
    tf = tar.extractfile(unlabeledname)
    for line in tf:
        line = line.decode("utf-8")
        text = line.strip()
        unlabeled.data.append(text)
        
            
    unlabeled.X = sentiment.count_vect.transform(unlabeled.data)
    print(unlabeled.X.shape)
    tar.close()
    return unlabeled


# In[5]:


def read_tsv(tar, fname):
    member = tar.getmember(fname)
    print(member.name)
    tf = tar.extractfile(member)
    data = []
    labels = []
    for line in tf:
        line = line.decode("utf-8")
        (label,text) = line.strip().split("\t")
        labels.append(label)
        data.append(text)
    return data, labels


# In[6]:


import matplotlib.pyplot as plt


# In[7]:


if __name__ == "__main__":
    # using token pattern only
    print("using token pattern only")
    for n in range(1,2):
        x = [i for i in range(1,11)]
        y1 = []
        y2 = []
        for c in range(1,11):
            print('n:%d c:%d'%(n,c))
            print("Reading data")
            tarfname = "data/sentiment.tar.gz"
            sentiment = read_files_token_pattern(tarfname,n)
            print("\nTraining classifier")
            import classify
            cls = classify.train_classifier(sentiment.trainX, sentiment.trainy,c)
            print("\nEvaluating")
            y1.append(classify.evaluate(sentiment.trainX, sentiment.trainy, cls, 'train'))
            y2.append(classify.evaluate(sentiment.devX, sentiment.devy, cls, 'dev'))
        
#         plt.plot(x, y1,label='accuracy on train', color='black', linestyle=':', marker='o')
#         plt.plot(x, y2,label='accuracy on dev', color='red',linestyle='--', marker='o')
#         for i in range(len(y1)):
#             plt.text(x[i], y1[i] - 0.01, '%.3f' %y1[i])
#         for i in range(len(y2)):
#             plt.text(x[i], y2[i] + 0.01, '%.3f' %y2[i])

#         plt.xticks(x)
        
#         plt.xlabel("C")
#         plt.ylabel("accuracy")
#         plt.title('n = %d Accuracy'%(n))
        
#         plt.legend(loc='upper left')
#         plt.grid()
#         plt.show()
    
    # using stop words only
    print("using stop words only")
    for n in range(1,2):
        x = [i for i in range(1,11)]
        y1 = []
        y2 = []
        for c in range(1,11):
            print('n:%d c:%d'%(n,c))
            print("Reading data")
            tarfname = "data/sentiment.tar.gz"
            sentiment = read_files_stop_words(tarfname,n)
            print("\nTraining classifier")
            import classify
            cls = classify.train_classifier(sentiment.trainX, sentiment.trainy,c)
            print("\nEvaluating")
            y1.append(classify.evaluate(sentiment.trainX, sentiment.trainy, cls, 'train'))
            y2.append(classify.evaluate(sentiment.devX, sentiment.devy, cls, 'dev'))
        
#         plt.plot(x, y1,label='accuracy on train', color='black', linestyle=':', marker='o')
#         plt.plot(x, y2,label='accuracy on dev', color='red',linestyle='--', marker='o')
#         for i in range(len(y1)):
#             plt.text(x[i], y1[i] - 0.01, '%.3f' %y1[i])
#         for i in range(len(y2)):
#             plt.text(x[i], y2[i] + 0.01, '%.3f' %y2[i])

#         plt.xticks(x)
        
#         plt.xlabel("C")
#         plt.ylabel("accuracy")
#         plt.title('n = %d Accuracy'%(n))
        
#         plt.legend(loc='upper left')
#         plt.grid()
#         plt.show()
        
    # using token pattern and stop words
    print("using token pattern and stop words")
    for n in range(1,2):
        x = [i for i in range(1,11)]
        y1 = []
        y2 = []
        for c in range(1,11):
            print('n:%d c:%d'%(n,c))
            print("Reading data")
            tarfname = "data/sentiment.tar.gz"
            sentiment = read_files_token_pattern_stop_words(tarfname,n)
            print("\nTraining classifier")
            import classify
            cls = classify.train_classifier(sentiment.trainX, sentiment.trainy,c)
            print("\nEvaluating")
            y1.append(classify.evaluate(sentiment.trainX, sentiment.trainy, cls, 'train'))
            y2.append(classify.evaluate(sentiment.devX, sentiment.devy, cls, 'dev'))
        
#         plt.plot(x, y1,label='accuracy on train', color='black', linestyle=':', marker='o')
#         plt.plot(x, y2,label='accuracy on dev', color='red',linestyle='--', marker='o')
#         for i in range(len(y1)):
#             plt.text(x[i], y1[i] - 0.01, '%.3f' %y1[i])
#         for i in range(len(y2)):
#             plt.text(x[i], y2[i] + 0.01, '%.3f' %y2[i])

#         plt.xticks(x)
        
#         plt.xlabel("C")
#         plt.ylabel("accuracy")
#         plt.title('n = %d Accuracy'%(n))
        
#         plt.legend(loc='upper left')
#         plt.grid()
#         plt.show()


# In[ ]:




