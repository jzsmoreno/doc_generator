# Breast Cancer Classification with Deep Learning

## 1. Introduction

This Jupyter Notebook demonstrates a deep learning approach to classifying breast cancer using the Wisconsin Breast Cancer dataset. The primary goal is to train an autoencoder model, followed by a classifier, to accurately predict whether a given image represents malignant or benign tissue. This project showcases the application of convolutional neural networks (CNNs) for feature extraction and classification in medical imaging.

## 2. Methodology

The methodology employed involves several key steps:

1.  **Data Loading and Preparation:** The Wisconsin Breast Cancer dataset is loaded using `sklearn.datasets`. The data is then converted into a Pandas DataFrame for easier manipulation. One-hot encoding is applied to the target variable (cancer status) to prepare it for classification with a multi-class model.
2.  **Autoencoder Training:** An autoencoder model is created, consisting of an encoder and a decoder. The encoder learns to compress the input image features into a lower-dimensional representation, while the decoder attempts to reconstruct the original image from this compressed representation. This process forces the network to learn robust and informative features.
3.  **Classifier Training:** A classifier layer is added on top of the encoder’s output. This classifier uses the encoded features to predict the cancer status (malignant or benign).
4.  **Model Compilation and Training:** The model is compiled using an Adam optimizer, which adjusts the network’s parameters during training to minimize the loss function. The categorical crossentropy loss function is used for multi-class classification. The model is trained for 15 epochs with a validation split to monitor performance and prevent overfitting.
5.  **Evaluation:** After training, the model's performance is evaluated on the test dataset using metrics such as accuracy, precision, recall, and F1-score. Cohen’s Kappa provides an assessment of agreement between predicted and actual labels, accounting for chance.

## 3. Analysis and Results

**Table 1: Model Performance Metrics**

| Metric           | Value        |
|------------------|--------------|
| Accuracy         | 92.44%       |
| Precision        | 91.10%       |
| Recall           | 97.48%       |
| F1-Score         | 94.18%       |
| Cohen’s Kappa    | 0.8344       |

These metrics demonstrate the effectiveness of the deep learning model in classifying breast cancer images. The high accuracy (92.44%) indicates that the model correctly classifies a large proportion of the test samples.  The F1-score of 94.18 further highlights the balanced performance between precision and recall, suggesting that the model effectively identifies both positive and negative cases. Cohen’s Kappa value of 0.8344 shows strong agreement between predicted and actual labels, indicating a robust classification system.

**Table 2: Hyperparameter Settings**

| Parameter          | Value        |
|--------------------|--------------|
| Activation         | selu         |
| Units              | 17           |
| Optimizer          | adam         |
| Epochs             | 15           |
| Loss Function      | CategoricalCrossentropy |

## 4. Conclusions

Based on the results, the trained autoencoder-classifier model demonstrates strong performance in classifying breast cancer images. The high accuracy, precision, recall, and F1-score indicate that the model effectively learned to distinguish between malignant and benign tissue.  The Cohen’s Kappa value of 0.8344 suggests a reliable classification system with minimal chance agreement. Further improvements could be achieved by exploring different network architectures, optimizing hyperparameters, or incorporating additional features into the training data. The use of an autoencoder allows for efficient feature extraction, which is crucial for achieving high classification accuracy in this medical imaging task.