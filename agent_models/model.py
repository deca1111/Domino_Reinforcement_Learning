import numpy
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import os


class Linear_QNet(nn.Module):
    def __init__(self, inputSize, hiddenSize, outputSize):
        super().__init__()
        self.entryLayer = nn.Linear(inputSize, hiddenSize[0])
        self.hiddenLayer = []
        self.hiddenLayer.extend(
            nn.Linear(hiddenSize[index], hiddenSize[index + 1])
            for index in range(len(hiddenSize) - 1)
            )
        self.exitLayer = nn.Linear(hiddenSize[-1], outputSize)
        # print(self.hiddenLayer)

    def forward(self, x):
        x = F.relu(self.entryLayer(x))
        for layer in self.hiddenLayer:
            x = layer(x)
        x = self.exitLayer(x)

        return x

    def save(self, fileName="model.pth"):
        torch.save(self.state_dict(), fileName)


class QTrainer:
    def __init__(self, model: Linear_QNet, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model

        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def trainStep(self, state, action, reward, nextState, done):
        # state = numpy.array(state)
        # nextState = numpy.array(nextState)
        state = torch.tensor(state, dtype=torch.float)
        nextState = torch.tensor(nextState, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        # Cas ou la dimension des données est 1
        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            nextState = torch.unsqueeze(nextState, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)

            done = (done,)

        # 1: Q value prédite à partir de l'état actuel
        pred = self.model(state)

        # 2: QNew = r + y * max(next pred Q value) -> only if not done
        target = pred.clone()
        for index in range(len(done)):
            QNew = reward[index]
            if not done[index]:
                QNew = reward[index] + self.gamma * torch.max(self.model(nextState[index]))

            target[index][torch.argmax(action).item()] = QNew

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()
