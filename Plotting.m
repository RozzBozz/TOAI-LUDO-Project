%% Plotting Q-value for experiment
clear
close all
clc
filepath = 'dataAnalysis/deltaQFig.txt';
myTable = readtable(filepath);
data = myTable{1,:};
figure(1)
plot(1:size(myTable,2),data)
xlabel('Episode number')
ylabel('Sum of ∆Q(s,a)-values)')

%% Plotting win rates for different learning rates / discount factors
clear
close all
clc
folder = 'dataAnalysis/HyperParameterTuning/';
alphaValues = [0.1, 0.2, 0.3, 0.4, 0.5];
gammaValues = [0.4, 0.5, 0.6, 0.7, 0.8];
useAlpha = false;
filepaths = [];
legendTitles = [];
if useAlpha == true
    for i = 1:size(alphaValues,2)
        filepaths{i} = strcat(folder,'epsilonDecay0.02alpha',num2str(alphaValues(i)),'gamma0.8.txt');
    end
else
    for i = 1:size(gammaValues,2)
        filepaths{i} = strcat(folder,'epsilonDecay0.02alpha0.25gamma',num2str(gammaValues(i)),'.txt');
    end
end
myTable1 = readtable(filepaths{1});
data1 = myTable1{1,:};
myTable2 = readtable(filepaths{2});
data2 = myTable2{1,:};
myTable3 = readtable(filepaths{3});
data3 = myTable3{1,:};
myTable4 = readtable(filepaths{4});
data4 = myTable4{1,:};
myTable5 = readtable(filepaths{5});
data5 = myTable5{1,:};
winRates = [data1(end), data2(end), data3(end), data4(end), data5(end)];
if useAlpha == true
    for i = 1:size(alphaValues,2)
        legendTitles{i} = strcat('α=', num2str(alphaValues(i)), ' WR:', num2str(winRates(i)), '%');
    end
else
    for i = 1:size(gammaValues,2)
        legendTitles{i} = strcat('γ=', num2str(gammaValues(i)), ' WR:', num2str(winRates(i)), '%');
    end
end
figure(1)
hold on
plot(1:size(myTable1,2),data1)
plot(1:size(myTable1,2),data2)
plot(1:size(myTable1,2),data3)
plot(1:size(myTable1,2),data4)
plot(1:size(myTable1,2),data5)
if useAlpha == true
    title('AIs trained with different learning rates γ=0.8, ε=1')
    legend(legendTitles{1},legendTitles{2},legendTitles{3},legendTitles{4},legendTitles{5})
else
    title('AIs trained with different discound factors. α=0.25, ε=1')
    legend(legendTitles{1},legendTitles{2},legendTitles{3},legendTitles{4},legendTitles{5})
end
xlabel('Episode number')
ylabel('Cumulative win rate [%]')
hold off

%% Plotting average win rates
clear
close all
clc
trainNumber = 1;
playNumber = 1;
filepathWin = strcat('dataAnalysis/winRateTesting/Train',num2str(trainNumber),'Play',num2str(playNumber),'WinRates.txt');
myTable1 = readtable(filepathWin);
cumulativeWinRates = myTable1{:,:};
avgWinRate = mean(cumulativeWinRates);
stdDev = std(avgWinRate);
f = figure(1);
hold on
plot(1:size(avgWinRate,2),avgWinRate)
hold off
if playNumber == 1
    text = ' one player,';
else
    text = ' three players,';
end
if trainNumber == 1
    text2 = ' one player';
else
    text2 = ' three players';
end
title(strcat('Trained on ', text2, ' played versus ', text, ' WR:',num2str(avgWinRate(end)),'% ±',num2str(stdDev)))
f.Position = [300,300,600,500];
xlabel('Episode number')
ylabel('Average cumulative win rate [%]')

%% Test for even mean
playOnOne = true;
if playOnOne == true
    filepath1 = 'dataAnalysis/winRateTesting/Train1Play1WinRates.txt';
    filepath2 = 'dataAnalysis/winRateTesting/Train3Play1WinRates.txt';
else
    filepath1 = 'dataAnalysis/winRateTesting/Train1Play3WinRates.txt';
    filepath2 = 'dataAnalysis/winRateTesting/Train3Play3WinRates.txt';
end
myTable1 = readtable(filepath1);
data1 = myTable1{:,:};
myTable2 = readtable(filepath2);
data2 = myTable2{:,:};
[h,p] = ttest2(data1(:,end),data2(:,end))