#!/bin/bash
cd ~/Dropbox/Purdue/CS590/hw1/

./../../nlp/project1/svml/svmlight/svm_learn train_dataset4svm_0.csv model0
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_0.csv model0

./../../nlp/project1/svml/svmlight/svm_learn train_dataset4svm_1.csv model1
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_1.csv model1

./../../nlp/project1/svml/svmlight/svm_learn train_dataset4svm_2.csv model2
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_2.csv model2

./../../nlp/project1/svml/svmlight/svm_learn -t 2 train_dataset4svm_0.csv model0
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_0.csv model0

./../../nlp/project1/svml/svmlight/svm_learn -t 2 train_dataset4svm_1.csv model1
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_1.csv model1

./../../nlp/project1/svml/svmlight/svm_learn -t 2 train_dataset4svm_2.csv model2
./../../nlp/project1/svml/svmlight/svm_classify test_dataset4svm_2.csv model2
