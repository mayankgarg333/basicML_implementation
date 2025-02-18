import numpy as np
import os
from sklearn import linear_model, datasets
import matplotlib.pyplot as plt



class Config:
    nn_input_dim = 2  # input layer dimensionality
    nn_output_dim = 2  # output layer dimensionality
    # Gradient descent parameters (I picked these by hand)
    epsilon = 0.01  # learning rate for gradient descent
    reg_lambda = 0.01  # regularization strength
    
    
def main():
    plt.close('all')
    # Generate a dataset and plot it
    np.random.seed(0)
    X, y = datasets.make_moons(200, noise=0.20)
    print  type(y)
    plt.figure(1)
    plt.scatter(X[:,0], X[:,1], s=80, c=y, cmap=plt.cm.Spectral)
    # Train the logistic rgeression classifier
    clf = linear_model.LogisticRegressionCV()
    clf.fit(X, y)
    # Plot the decision boundary
    f2=plt.figure(2)
    plot_decision_boundary(lambda x: clf.predict(x),X,y)
    plt.title("Logistic Regression")
   
    # Build a model with a 3-dimensional hidden layer
    model = build_model(X,y,3, print_loss=True)
    f3=plt.figure(3)
    plot_decision_boundary(lambda x: predict(model,x), X, y)
    plt.title("Neural network")
    return model


# This function learns parameters for the neural network and returns the model.
# - nn_hdim: Number of nodes in the hidden layer
# - num_passes: Number of passes through the training data for gradient descent
# - print_loss: If True, print the loss every 1000 iterations
def build_model(X,y,nn_hdim, num_passes=10000, print_loss=False):
    num_examples = len(X)
    # Initialize the parameters to random values. We need to learn these.
    np.random.seed(0)
    W1 = np.random.randn(Config.nn_input_dim, nn_hdim) / np.sqrt(Config.nn_input_dim)
    b1 = np.zeros((1, nn_hdim))
    W2 = np.random.randn(nn_hdim, Config.nn_output_dim) / np.sqrt(nn_hdim)
    b2 = np.zeros((1, Config.nn_output_dim))
 
    # This is what we return at the end
    model = {}
    # Gradient descent. For each batch...
    for i in xrange(0, num_passes):
         # Forward propagation
        z1 = X.dot(W1) + b1
        a1 = sigmoid(z1)
        z2 = a1.dot(W2) + b2
        #exp_scores = np.exp(z2)
        #probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
        probs= sigmoid(z2)
        # Backpropagation
        delta3 = probs
        #print [range(num_examples), y]
        delta3[range(num_examples), y] -= 1
        dW2 = (a1.T).dot(delta3)
        db2 = np.sum(delta3, axis=0, keepdims=True)
        #delta2 = delta3.dot(W2.T) * (1 - np.power(a1, 2))
        delta2 = delta3.dot(W2.T) * a1*(1 - a1)
        dW1 = np.dot(X.T, delta2)
        db1 = np.sum(delta2, axis=0)
 
        # Add regularization terms (b1 and b2 don't have regularization terms)
        dW2 += Config.reg_lambda * W2
        dW1 += Config.reg_lambda * W1
 
        # Gradient descent parameter update
        W1 += -Config.epsilon * dW1
        b1 += -Config.epsilon * db1
        W2 += -Config.epsilon * dW2
        b2 += -Config.epsilon * db2
         
        # Assign new parameters to the model
        model = { 'W1': W1, 'b1': b1, 'W2': W2, 'b2': b2}
         
        # Optionally print the loss.
        # This is expensive because it uses the whole dataset,
        if print_loss and i % 1000 == 0:
          print "Loss after iteration %i: %f" %(i, calculate_loss(model,X,y))
    return model
    

# Helper function to evaluate the total loss on the dataset
def calculate_loss(model,X,y):
    num_examples = len(X)
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    #print X.shape, W1.shape, b1.shape, W2.shape, b2.shape
    # Forward propagation to calculate our predictions
    z1 = X.dot(W1) + b1
    a1 = sigmoid(z1)            # function in layer 1
    z2 = a1.dot(W2) + b2
    probs= sigmoid(z2)
    #exp_scores = np.exp(z2)     
    #probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    # Calculating the loss
    b=range(num_examples), y
    VV=0
    for i in range(len(b[0])):
        VV=VV-np.log(probs[b[0][i],b[1][i]])
    data_loss=VV
#    corect_logprobs = -np.log(probs[range(num_examples), y])
#    data_loss = np.sum(corect_logprobs)
    # Add regulatization term to loss (optional)
    data_loss += Config.reg_lambda/2 * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
    return 1./num_examples * data_loss
    
    
    
def plot_decision_boundary(pred_func,X,y):
    # Set min and max values and give it some padding
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    h = 0.01
    # Generate a grid of points with distance h between them
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # Predict the function value for the whole gid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])  #np.vstack((xx.ravel(), yy.ravel())).T
    Z = Z.reshape(xx.shape)
    # Plot the contour and training examples
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral)
    plt.scatter(X[:, 0], X[:, 1],  s=80, c=y, cmap=plt.cm.Spectral)
    plt.axis([x_min,x_max,y_min,y_max  ])
    
    
def predict(model, x):
    W1, b1, W2, b2 = model['W1'], model['b1'], model['W2'], model['b2']
    # Forward propagation
    z1 = x.dot(W1) + b1
    a1 = np.tanh(z1)
    z2 = a1.dot(W2) + b2
    probs= sigmoid(z2)
    #exp_scores = np.exp(z2)
    #probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
    return np.argmax(probs, axis=1)

def sigmoid(x):
  return 1 / (1 + np.exp(-x))
    
model=main()