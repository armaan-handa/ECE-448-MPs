# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019

"""
You should only modify code within this file for part 2 -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class NeuralNet(torch.nn.Module):
    def __init__(self, lrate,loss_fn,in_size,out_size):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        @param loss_fn: The loss functions
        @param in_size: Dimension of input
        @param out_size: Dimension of output
        """
        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn
        self.l1 = nn.Linear(in_size, 128)
        self.l2 = nn.Linear(128, out_size)
        # self.l3 = nn.Linear(512, 320)
        # self.l4 = nn.Linear(320, out_size)
        # self.l5 = nn.Linear(450, out_size)
        self.optimizer = optim.SGD(self.get_parameters(), lr=lrate)


    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters()

    def forward(self, x):
        """ A forward pass of your autoencoder
        @param x: an (N, in_size) torch tensor
        @return y: an (N, out_size) torch tensor of output from the network
        """
        x = F.relu(self.l1(x))
        # x = F.relu(self.l2(x))
        # x = F.relu(self.l3(x))
        # x = F.tanh(self.l4(x))
        x = self.l2(x)
        return x

    def step(self, x,y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, in_size) torch tensor
        @param y: an (N,) torch tensor
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        self.optimizer.zero_grad()
        yhat = self.forward(x)
        loss = self.loss_fn(yhat, y)
        L = loss.backward()
        self.optimizer.step()
        return loss



def fit(train_set,train_labels,dev_set,n_iter,batch_size=100):
    """ Fit a neural net.  Use the full batch size.
    @param train_set: an (N, 784) torch tensor
    @param train_labels: an (N,) torch tensor
    @param dev_set: an (M, 784) torch tensor
    @param n_iter: int, the number of batches to go through during training (not epoches)
                   when n_iter is small, only part of train_set will be used, which is OK,
                   meant to reduce runtime on autograder.
    @param batch_size: The size of each batch to train on.
    # return all of these:
    @return losses: list of total loss (as type float) after each iteration. Ensure len(losses) == n_iter
    @return yhats: an (M,) NumPy array of approximations to labels for dev_set
    @return net: A NeuralNet object
    # NOTE: This must work for arbitrary M and N
    """

    in_size = 784
    out_size = 5
    lrate = 0.2
    loss_fn = nn.CrossEntropyLoss()
    net = NeuralNet(lrate, loss_fn, in_size, out_size)
    length = len(train_set)
    # print(length)
    losses = []
    yhats = []
    train_set_std = (train_set- train_set.mean(dim=-2, keepdim=True))/train_set.std(dim=-2, keepdim=True)
    for n in range(n_iter):
        losses.append(net.step(train_set_std[(n*batch_size)%length : ((n+1)*batch_size)%length], train_labels[(n*batch_size)%length : ((n+1)*batch_size)%length]).item())
    dev_set_std = (dev_set - train_set.mean(dim=-2, keepdim=True))/train_set.std(dim=-2, keepdim=True)
    output = net.forward(dev_set_std)
    for n in range(len(dev_set)):
        yhats.append(np.argmax(output[n].detach().numpy()))
    torch.save(net, 'net_p2.model')
    # print(losses)
    return losses,yhats, net