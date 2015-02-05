#!/bin/bash
cd ~/Dropbox/Purdue/nlp/project1/doc2vec/

../svml/svmlight/svm_learn train_dataset4svm_0.csv model0
../svml/svmlight/svm_classify test_dataset4svm_0.csv model0

../svml/svmlight/svm_learn train_dataset4svm_1.csv model1
../svml/svmlight/svm_classify test_dataset4svm_1.csv model1

../svml/svmlight/svm_learn train_dataset4svm_2.csv model2
../svml/svmlight/svm_classify test_dataset4svm_2.csv model2

../svml/svmlight/svm_learn train_dataset4svm_3.csv model3
../svml/svmlight/svm_classify test_dataset4svm_3.csv model3

../svml/svmlight/svm_learn train_dataset4svm_4.csv model4
../svml/svmlight/svm_classify test_dataset4svm_4.csv model4

../svml/svmlight/svm_learn train_dataset4svm_0.csv -t 2 model0
../svml/svmlight/svm_classify test_dataset4svm_0.csv model0

../svml/svmlight/svm_learn train_dataset4svm_1.csv -t 2 model1
../svml/svmlight/svm_classify test_dataset4svm_1.csv model1

../svml/svmlight/svm_learn train_dataset4svm_2.csv -t 2 model2
../svml/svmlight/svm_classify test_dataset4svm_2.csv model2

../svml/svmlight/svm_learn train_dataset4svm_3.csv -t 2 model3
../svml/svmlight/svm_classify test_dataset4svm_3.csv model3

../svml/svmlight/svm_learn train_dataset4svm_4.csv -t 2 model4
../svml/svmlight/svm_classify test_dataset4svm_4.csv model4
