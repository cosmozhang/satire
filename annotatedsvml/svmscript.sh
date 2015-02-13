#!/bin/bash
cd ~/Dropbox/Purdue/nlp/project1/annotatedsvml/
export PYTHONPATH=${PYTHONPATH}:~/Dropbox/Purdue/nlp/project1/annotatedsvml/

echo 'start svmlight'
export st=0
export fn=5
echo $st
echo $fn

echo 'binary'
python gensvminput.py -B
for (( i=$st; i<$fn; i++ ))
do
    echo $i
	../svml/svmlight/svm_learn binary_train_dataset4svm_${i}.csv model${i}
	../svml/svmlight/svm_classify binary_test_dataset4svm_${i}.csv model${i}
done

echo 'frequency'
python gensvminput.py -F
for (( i=$st; i<$fn; i++ ))
do
    echo $i
../svml/svmlight/svm_learn frequency_train_dataset4svm_${i}.csv model${i}
../svml/svmlight/svm_classify frequency_test_dataset4svm_${i}.csv model${i}
done

echo 'speaker'
python gensvminput.py -S
for (( i=$st; i<$fn; i++ ))
do
    echo $i
../svml/svmlight/svm_learn speaker_train_dataset4svm_${i}.csv model${i}
../svml/svmlight/svm_classify speaker_test_dataset4svm_${i}.csv model${i}
done

echo 'quote'
python gensvminput.py -Q
for (( i=$st; i<$fn; i++ ))
do
    echo $i
../svml/svmlight/svm_learn quote_train_dataset4svm_${i}.csv model${i}
../svml/svmlight/svm_classify quote_test_dataset4svm_${i}.csv model${i}
done

echo 'original'
python gensvminput.py -O
for (( i=$st; i<$fn; i++ ))
do
    echo $i
../svml/svmlight/svm_learn original_train_dataset4svm_${i}.csv model${i}
../svml/svmlight/svm_classify original_test_dataset4svm_${i}.csv model${i}
done