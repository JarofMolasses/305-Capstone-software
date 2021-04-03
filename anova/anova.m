% run one-way ANOVA on hand-compiled tables from the filter tests
% matlab could actually run the entire operation start to
% finish - read the raw time-series data, generate the tables, and process them
% we'll do all that later. also python is probably better

% NOTE: matlab anova will only work with matrices, so no tables

% Read in hand-compiled tables from spreadsheet (lame, yes i know)
% Columns are different filter stacks (1-none, 2-carbon, 3-HEPA) 
integrated = readmatrix('Processing - Integrated ANOVA.csv');
peak = readmatrix('Processing - Peak ANOVA.csv');

group =  {'Control', 'Carbon', 'HEPA'};
    
[p, table, stats] = anova1(integrated,group);
comp = multcompare(stats);

p % the p(F) for the one way ANOVA
p12 = comp(1,end)  % p-value for means of carbon, control
p13 = comp(2,end)  % p-value for means of HEPA, control
p23 = comp(3,end)  % p-value for means of HEPA, carbon

