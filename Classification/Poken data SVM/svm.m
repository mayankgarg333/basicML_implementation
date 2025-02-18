clear all; close all; clc


% ADD LIBSVM library, Library is precomplied. 
addpath(genpath('lib\'))

% Load data
load poker_train.data
load poker_test.data
poker_i=[poker_train;poker_test];
poker_i(:,end)=poker_i(:,end)+1;

k=1;
%Generate new features 
for i = 1:2:9
    for j= i+2:2:9
        X(:,k)=abs(poker_i(:,i)-poker_i(:,j));
        k=k+1;
    end
end
%Generate new features 
for i = 2:2:10
    for j= i+2:2:10
        X(:,k)=abs(poker_i(:,i)-poker_i(:,j));
        k=k+1;
    end
end

X(:,end+1)=poker_i(:,end);
poker=X;


gamma=1E-3;
result=[];
for j=1:30  % loop to get a ballpark value of Gamma
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
train1 = []; %stores the training samples
test = [];  %stores the test samples
for i=1:10  
    ind{i} = find(poker(:,end)==i);
    len = length(ind{i});
    t = randperm(len);
    half = round(len/20);
    train1 = [train1; poker(ind{i}(t(1:half)), :)];
    test = [test; poker(ind{i}(t(half+1:2*half)), :)];
end

% write data in the required format

train_mat=train1(:,1:end-1);
train_y=train1(:,end);
test_mat=test(:,1:end-1);
test_y=test(:,end);
labels = train_y; % labels from the 1st column
features = train_mat; 
features_sparse = sparse(features); % features must be in a sparse matrix
libsvmwrite('train.data', labels, features_sparse);
labels = test_y; % labels from the 1st column
features = test_mat; 
features_sparse = sparse(features); % features must be in a sparse matrix
libsvmwrite('test.data', labels, features_sparse);

% Read data and train the model

gamma=gamma*(1.2);
[y, x] = libsvmread('train.data');
% Libsvm options
% -s 0 : classification
% -t 2 : RBF kernel
% -g : gamma in the RBF kernel

model = svmtrain(y, x, sprintf('-s 0 -t 2 -g %g', gamma));


%%%%%%%%%%%%%%%%%%%%%%%%%% NOTE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% It is important to remember here that the value changed in gamma not sigma
% gamma = 1/ sigma; 
% RBF kernal = EXP(-NORM(x1-x1)/sigma)== EXP(-NORM(x1-x1)* gamma)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Calculate training accuracy
w = model.SVs' * model.sv_coef;
b = -model.rho;
if (model.Label(1) == -1)
    w = -w; b = -b;
end
[predicted_label, accuracy, decision_values] = svmpredict(y, x, model);

% Calculate Test set accuracy
[test_y, test_x] = libsvmread('test.data');%
[predicted_label2, accuracy2, decision_values2] = svmpredict(test_y, test_x, model);

result(j,1:3)=[gamma accuracy(1) accuracy2(1)]

end

save All_results

% After calculating the accuracy for different gamma value, Fine tune Gamma value seprately 
% to achieve higher accuracy
