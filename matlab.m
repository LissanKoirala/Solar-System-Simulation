formatSpec = '%f';

fileID = fopen('speed.txt','r');
speed = fscanf(fileID,formatSpec);

% fileID = fopen('comet_halley/distance_only.csv','r');
% data1 = fscanf(fileID,formatSpec);

plot(speed, 'r')
title('Combine Plots')

% hold on

%  plot(data1, 'g')
