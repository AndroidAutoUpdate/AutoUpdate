# AutoUpdate
The replication package is created for the paper titled "AutoUpdate: Automatically Recommend Code Updates for Android Apps"
## Overview

## Description

## Dataset 
Since there is no publicly-available datasets of code updates for Android apps, we construct a new dataset to evaluate the performance of automatically recommending code updates for Android apps.  We collect 209,346 pairs of updated methods from 3,195 open-source Android applications. 

The datasets are publicly available at Zenodo [Link](https://zenodo.org/record/6538487).

## Gettting Started
### Prerequisite

- Python 3.6 +
- Packages:

```shell
pip install -r requirements.txt
```


### The architecture of AutoUpdate
```shell
cd model/
```
#### Parameters
- ``<data_dir>``: the directory path to the dataset of the original code of changed methods
- ``<tokenized_data_dir>``: the directory for storing the subword tokenized data with the same structure as above.
- ``<num_merges>``: The number of merge operations
- ``<binary_data_dir>``: the directory for storing the binary data for tensor2tensor
- ``<hyper-parameter_setting>: the setting name of the hyper-parameters defined in ``AutoTransform/AutoTransform_problem.py``
- ``<model_dir>``: the directory for saving the model
- ``<train_step>``: the number of train steps to train model
- ``<input_file>``: the text file of the before version in the testing data
- ``<ckpt_number>``: the checkpoint number (i.e., the number of train steps that the model was used to train). For example, ``ckpt_number=1000`` means that  we will use the model that was trained using 1000 train steps.
- ``<beam_width>``: the number of generated sequences for each input instance (i.e., a method)

#### (1) Code Abstraction
Please use src2abs (more information are available [here](https://github.com/micheletufano/src2abs)) for code abstraction

```shell
git clone https://github.com/micheletufano/src2abs.git
```


#### (2) BPE subword Tokenization
This script will perform BPE subword tokenization the abstracted data.

```
bash subword_tokenize.sh <data_dir> <tokenized_data_dir> <num_merges>
```


#### (3) Training stage
This script will convert the text files of the before and after versions in the training and validation data into binary files.

```
bash generate_binary_data.py <data_dir> <binary_data_dir>
```


This script will train the Transformer model based on the specified hyper-parameter setting and the number of train steps

```
bash train_model.sh <binary_data_dir> <hyper-parameter_setting> <model_dir> <train_step>
```


#### (4) Inference stage
This script will generate a prediction for each method in the input_file. The output will be saved under the model directory (i.e., ``<model_dir>/predictions``)

```
bash inference.sh <binary_data_dir> <model_dir> <input_file> <hyper-parameter_setting> <ckpt_number> <beam_width>
```

### Evaluation
```
cd evaluation/
```

#### Parameters
- ``<generated_prediction_path>``: the path of the generated prediciton file by Transformer
- ``<decoded_prediction_path>``: the path to save the decoded prediciton file

#### (1) Decoding generated predictions
This script will convert subwords into code.

```
python code_decode.py <generated_prediction_path> <decoded_prediction_path>
```

#### (2) Generating evaluation metrics
This script will calculate the evaluation metrics (i.e., #perfect prediction, accuracy, CodeBLEU) for the predictions.

```
python code_decode.py <decoded_prediction_path> <reference_path> <beam_size>
```