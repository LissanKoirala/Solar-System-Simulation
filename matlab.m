formatSpec = '%f';

fileID = fopen('distance_between.txt','r');
data = fscanf(fileID,formatSpec);

% fileID = fopen('comet_halley/distance_only.csv','r');
% data1 = fscanf(fileID,formatSpec);

plot(data, 'r')
title('Combine Plots')

% hold on

%  plot(data1, 'g')
