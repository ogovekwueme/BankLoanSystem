import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split 
from sklearn.metrics import accuracy_score, confusion_matrix
from features import features # getting the features needed for this project
from features import target # getting the target


data = pd.read_csv('lending-club-data.csv',low_memory=False)
data['safe_loans'] = data['bad_loans'].apply((lambda x: +1 if x== 0 else -1))
#ddata = data.dropna() #dropping data wih null values
loans = data[features +[target]]
#print loans.shape

cats = []
ccols = []
for c,d in zip(loans.columns, loans.dtypes):
  if d == object:
    cats.append(c)


# one hot encoding....
print 'Performing One hot encoding...'
cat_loans = loans[cats]
cloans = pd.get_dummies(cat_loans,prefix='feats_')

nloans = loans.drop(cats, axis=1)
newloans = cloans.join(nloans)

feats = newloans.drop(target,axis=1)
tars = newloans[target]

feat_train, feat_test, tar_train, tar_test =train_test_split(feats, tars, test_size=.3)

# running the RandomForest  classifier
print; print 'Running the Random Forest Classifier'
classifier = RandomForestClassifier()
rforest = classifier.fit(feat_train, tar_train)

# performing predictions
predictions = rforest.predict(feat_test)

#running the metrics

print 'Accuracy Score =',
print accuracy_score(predictions, tar_test)
print
print 'Confusion Matrix='
print confusion_matrix(predictions, tar_test)

