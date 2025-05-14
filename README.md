# Rema Intent Classifier Chatbot

We made a Chatbot that can recognize a user input's intents (limited to the context of our Dataset, which centers around student grade information) based off of a .json file filled with pre-generated intents and (possible) user input patterns.

The model uses TF-IDF to determine high weighted terms in a user input that could then indicate the model to classify it into a certain intent. To classify the user input itself, we used (scikit-learn's) Logistic Regression and have the model predict with intent tag the user input falls into by comparing it to classifiers for each intent.

Made by:
1. Aliya Cahyanti Wijaya
2. Melvin Wijaya
3. Regina Hillary

for our AI course's final project.
