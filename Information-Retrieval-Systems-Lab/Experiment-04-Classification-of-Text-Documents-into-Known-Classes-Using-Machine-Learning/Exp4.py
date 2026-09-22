import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

categories = [
    "comp.graphics",
    "rec.sport.baseball",
    "sci.space",
    "talk.politics.misc"
]

print("=" * 70)
print("IRS LAB - EXPERIMENT 4")
print("TEXT DOCUMENT CLASSIFICATION")
print("=" * 70)

print("\nLoading Training Dataset...")

train_data = fetch_20newsgroups(
    subset="train",
    categories=categories,
    remove=("headers", "footers", "quotes")
)

print("\nTraining Dataset Loaded Successfully")
print("Number of Training Documents:", len(train_data.data))
print("Number of Classes:", len(train_data.target_names))

print("\nClasses:")

for i, category in enumerate(train_data.target_names):
    print(i, ":", category)

print("\nLoading Testing Dataset...")

test_data = fetch_20newsgroups(
    subset="test",
    categories=categories,
    remove=("headers", "footers", "quotes")
)

print("\nTesting Dataset Loaded Successfully")
print("Number of Testing Documents:", len(test_data.data))

print("\n" + "=" * 70)
print("SAMPLE DOCUMENT")
print("=" * 70)

print(train_data.data[0][:1000])

print("\nActual Class:")

print(train_data.target_names[train_data.target[0]])

print("\n" + "=" * 70)
print("TF-IDF FEATURE EXTRACTION")
print("=" * 70)

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    max_df=0.95,
    min_df=2,
    ngram_range=(1, 2),
    max_features=20000
)

X_train = vectorizer.fit_transform(train_data.data)
X_test = vectorizer.transform(test_data.data)

y_train = train_data.target
y_test = test_data.target

print("\nTF-IDF Conversion Completed")
print("Training Matrix Shape:", X_train.shape)
print("Testing Matrix Shape:", X_test.shape)
print("Vocabulary Size:", len(vectorizer.vocabulary_))

print("\n" + "=" * 70)
print("NAIVE BAYES CLASSIFICATION")
print("=" * 70)

nb_classifier = MultinomialNB()

nb_classifier.fit(X_train, y_train)

nb_predictions = nb_classifier.predict(X_test)

nb_accuracy = accuracy_score(y_test, nb_predictions)

nb_precision = precision_score(
    y_test,
    nb_predictions,
    average="weighted",
    zero_division=0
)

nb_recall = recall_score(
    y_test,
    nb_predictions,
    average="weighted",
    zero_division=0
)

nb_f1 = f1_score(
    y_test,
    nb_predictions,
    average="weighted",
    zero_division=0
)

print("\nNaive Bayes Results")
print("-" * 50)

print("Accuracy  :", round(nb_accuracy, 4))
print("Precision :", round(nb_precision, 4))
print("Recall    :", round(nb_recall, 4))
print("F1-Score  :", round(nb_f1, 4))

print("\nNaive Bayes Classification Report")

print(
    classification_report(
        y_test,
        nb_predictions,
        target_names=train_data.target_names,
        zero_division=0
    )
)

print("\n" + "=" * 70)
print("SUPPORT VECTOR MACHINE CLASSIFICATION")
print("=" * 70)

svm_classifier = LinearSVC()

svm_classifier.fit(X_train, y_train)

svm_predictions = svm_classifier.predict(X_test)

svm_accuracy = accuracy_score(
    y_test,
    svm_predictions
)

svm_precision = precision_score(
    y_test,
    svm_predictions,
    average="weighted",
    zero_division=0
)

svm_recall = recall_score(
    y_test,
    svm_predictions,
    average="weighted",
    zero_division=0
)

svm_f1 = f1_score(
    y_test,
    svm_predictions,
    average="weighted",
    zero_division=0
)

print("\nSVM Results")
print("-" * 50)

print("Accuracy  :", round(svm_accuracy, 4))
print("Precision :", round(svm_precision, 4))
print("Recall    :", round(svm_recall, 4))
print("F1-Score  :", round(svm_f1, 4))

print("\nSVM Classification Report")

print(
    classification_report(
        y_test,
        svm_predictions,
        target_names=train_data.target_names,
        zero_division=0
    )
)

print("\n" + "=" * 70)
print("CLASSIFIER COMPARISON")
print("=" * 70)

results = pd.DataFrame({
    "Algorithm": [
        "Naive Bayes",
        "Support Vector Machine"
    ],
    "Accuracy": [
        nb_accuracy,
        svm_accuracy
    ],
    "Precision": [
        nb_precision,
        svm_precision
    ],
    "Recall": [
        nb_recall,
        svm_recall
    ],
    "F1-Score": [
        nb_f1,
        svm_f1
    ]
})

print("\n")
print(results.to_string(index=False))

plot_data = results.set_index("Algorithm")

plot_data.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Text Classification Algorithm Comparison")
plt.xlabel("Classification Algorithm")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

nb_cm = confusion_matrix(
    y_test,
    nb_predictions
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    nb_cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=train_data.target_names,
    yticklabels=train_data.target_names
)

plt.title("Naive Bayes Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.tight_layout()
plt.show()

svm_cm = confusion_matrix(
    y_test,
    svm_predictions
)

plt.figure(figsize=(8, 6))

sns.heatmap(
    svm_cm,
    annot=True,
    fmt="d",
    cmap="Greens",
    xticklabels=train_data.target_names,
    yticklabels=train_data.target_names
)

plt.title("SVM Confusion Matrix")
plt.xlabel("Predicted Class")
plt.ylabel("Actual Class")
plt.tight_layout()
plt.show()

class_counts = pd.Series(
    train_data.target
).value_counts().sort_index()

class_names = [
    train_data.target_names[i]
    for i in class_counts.index
]

plt.figure(figsize=(10, 6))

plt.bar(
    class_names,
    class_counts.values
)

plt.title("Training Document Distribution")
plt.xlabel("Document Class")
plt.ylabel("Number of Documents")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()

print("\n" + "=" * 70)
print("CLASSIFICATION OF NEW DOCUMENTS")
print("=" * 70)

new_documents = [
    """
    NASA launched a new spacecraft to explore planets,
    galaxies and objects in deep space.
    """,
    """
    The baseball team won the game after scoring
    five runs in the final inning.
    """,
    """
    The computer graphics system uses rendering,
    image processing and three dimensional visualization.
    """,
    """
    The government announced a new political policy
    after a long discussion in parliament.
    """
]

new_X = vectorizer.transform(new_documents)

new_predictions = svm_classifier.predict(new_X)

for i, prediction in enumerate(new_predictions):

    print("\nDocument", i + 1)

    print(new_documents[i].strip())

    print(
        "\nPredicted Class:",
        train_data.target_names[prediction]
    )

    print("-" * 60)

print("\n" + "=" * 70)
print("FINAL RESULT")
print("=" * 70)

print(
    "\nNaive Bayes Accuracy:",
    round(nb_accuracy * 100, 2),
    "%"
)

print(
    "SVM Accuracy:",
    round(svm_accuracy * 100, 2),
    "%"
)

if svm_accuracy > nb_accuracy:

    print(
        "\nSVM performed better than Naive Bayes "
        "for this experiment."
    )

elif nb_accuracy > svm_accuracy:

    print(
        "\nNaive Bayes performed better than SVM "
        "for this experiment."
    )

else:

    print(
        "\nBoth classifiers produced the same accuracy."
    )

print("\nExperiment Completed Successfully.")