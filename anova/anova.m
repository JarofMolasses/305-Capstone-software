% run one-way ANOVA on hand-compiled tables from the filter tests
% matlab could actually run the entire operation start to
% finish - read the raw time-series data, generate the tables, and process them
% we'll do all that later. also python is probably better

% NOTE: matlab anova will only work with matrices, so no tables


clear;
close all;
% Read in hand-compiled tables from spreadsheet (lame, yes i know)
% Columns are different filter stacks (1-none, 2-carbon, 3-HEPA) 
intarray = readmatrix('Processing - Integrated ANOVA.csv');
peakarray = readmatrix('Processing - Peak ANOVA.csv');

group =  {'Control', 'Carbon', 'HEPA'};
    
[ppeak, ptable, peakstats] = anova1(peakarray,group);
[intpeak, inttable, intstats] = anova1(intarray,group);

figure;
pcomp = multcompare(peakstats);
figure;
intcomp = multcompare(intstats);

