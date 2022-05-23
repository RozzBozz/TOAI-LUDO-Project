filepath = 'deltaQs/epsilonDecay0alpha0.05gamma0.7.txt';
myTable = readtable(filepath);
data = myTable{1,:};
figure(1)
plot(1:size(myTable,2),data)

filepath = 'deltaQs/epsilonDecay0alpha0.5gamma0.9.txt';
myTable2 = readtable(filepath);
data2 = myTable2{1,:};
figure(2)
plot(1:size(myTable2,2),data2)