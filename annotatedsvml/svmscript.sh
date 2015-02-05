#!/bin/bash
cd ~/Dropbox/Purdue/nlp/project1/annotatedsvml/

../svml/svmlight/svm_learn binary_train_dataset4svm_0.csv model0
../svml/svmlight/svm_classify binary_test_dataset4svm_0.csv model0

../svml/svmlight/svm_learn binary_train_dataset4svm_1.csv model1
../svml/svmlight/svm_classify binary_test_dataset4svm_1.csv model1

../svml/svmlight/svm_learn binary_train_dataset4svm_2.csv model2
../svml/svmlight/svm_classify binary_test_dataset4svm_2.csv model2

../svml/svmlight/svm_learn binary_train_dataset4svm_3.csv model3
../svml/svmlight/svm_classify binary_test_dataset4svm_3.csv model3

../svml/svmlight/svm_learn binary_train_dataset4svm_4.csv model4
../svml/svmlight/svm_classify binary_test_dataset4svm_4.csv model4

../svml/svmlight/svm_learn frequency_train_dataset4svm_0.csv model0
../svml/svmlight/svm_classify frequency_test_dataset4svm_0.csv model0

../svml/svmlight/svm_learn frequency_train_dataset4svm_1.csv model1
../svml/svmlight/svm_classify frequency_test_dataset4svm_1.csv model1

../svml/svmlight/svm_learn frequency_train_dataset4svm_2.csv model2
../svml/svmlight/svm_classify frequency_test_dataset4svm_2.csv model2

../svml/svmlight/svm_learn frequency_train_dataset4svm_3.csv model3
../svml/svmlight/svm_classify frequency_test_dataset4svm_3.csv model3

../svml/svmlight/svm_learn frequency_train_dataset4svm_4.csv model4
../svml/svmlight/svm_classify frequency_test_dataset4svm_4.csv model4