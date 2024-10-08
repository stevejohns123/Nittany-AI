# -*- coding: utf-8 -*-
"""Digit Recognition with PyTorch
Original file is located at
    https://colab.research.google.com/drive/1ixOu1DE61NzDqaibojOlg3VwFA2vcSxG
# Digit Recognition with PyTorch

## Description
This project implements a neural network for recognizing handwritten digits using the MNIST dataset. It demonstrates fundamental concepts of deep learning such as model architecture, training, evaluation, and visualization of predictions using PyTorch. This project serves as an excellent starting point for beginners in machine learning and deep learning.

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/stevejohns123/digit_recognition_with_pytorch.git
   cd digit_recognition_with_pytorch
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install torch torchvision matplotlib numpy pandas
python digit_recognition_with_pytorch.py
Contributors
Steven Johnson (GitHub: stevejohns123)
References
Dataset: MNIST Dataset (Automatically downloaded through PyTorch's torchvision library)
Framework: PyTorch Documentation
Tutorials: Additional resources for understanding MNIST classification:
PyTorch MNIST Tutorial
Towards Data Science: Building Neural Networks with PyTorch
Code Standards
Follow PEP 8 standards for Python code.
Ensure that all functions and classes are properly documented.
Include comments to explain important parts of the code.
Licensing
This project is licensed under the MIT License. See the LICENSE file for more details.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, layers, models

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

# Define transformations for the training and test sets
transform = transforms.Compose([
    transforms.ToTensor(),  # Convert images to PyTorch tensors
    transforms.Normalize((0.5,), (0.5,))  # Normalize the images
])

# Load the MNIST dataset
train_set = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
test_set = datasets.MNIST(root='./data', train=False, download=True, transform=transform)

# Create data loaders
train_loader = DataLoader(train_set, batch_size=64, shuffle=True)
test_loader = DataLoader(test_set, batch_size=64, shuffle=False)

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128)  # Input layer (784) to hidden layer (128)
        self.fc2 = nn.Linear(128, 64)        # Hidden layer (128) to hidden layer (64)
        self.fc3 = nn.Linear(64, 10)         # Hidden layer (64) to output layer (10)

    def forward(self, x):
        x = x.view(-1, 28 * 28)  # Flatten the image
        x = torch.relu(self.fc1(x))  # Apply ReLU activation
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)  # No activation on the output layer
        return x

# Instantiate the model
model = NeuralNetwork()

criterion = nn.CrossEntropyLoss()  # Loss function
optimizer = optim.SGD(model.parameters(), lr=0.01)  # Optimizer

def train(model, train_loader, criterion, optimizer, epochs=5):
    model.train()  # Set the model to training mode
    for epoch in range(epochs):
        for images, labels in train_loader:
            optimizer.zero_grad()  # Zero the gradients
            outputs = model(images)  # Forward pass
            loss = criterion(outputs, labels)  # Compute loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update weights
        print(f'Epoch {epoch + 1}/{epochs}, Loss: {loss.item():.4f}')

# Train the model
train(model, train_loader, criterion, optimizer)

def evaluate(model, test_loader):
    model.eval()  # Set the model to evaluation mode
    correct = 0
    total = 0
    with torch.no_grad():  # Disable gradient calculation
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)  # Get the predicted labels
            total += labels.size(0)  # Update total
            correct += (predicted == labels).sum().item()  # Update correct predictions

    accuracy = 100 * correct / total
    print(f'Accuracy of the model on the test set: {accuracy:.2f}%')

# Evaluate the model
evaluate(model, test_loader)

def visualize_predictions(model, test_loader):
    model.eval()
    with torch.no_grad():
        images, labels = next(iter(test_loader))
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)

        # Plotting the images and predictions
        plt.figure(figsize=(10, 10))
        for i in range(25):
            plt.subplot(5, 5, i + 1)
            plt.imshow(images[i].numpy().squeeze(), cmap='gray')
            plt.title(f'True: {labels[i].item()}, Predicted: {predicted[i].item()}')
            plt.axis('off')
        plt.show()

# Visualize predictions
visualize_predictions(model, test_loader)
