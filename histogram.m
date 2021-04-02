clear;
close;

data = readtable('nofilter-distributiontest_20210402_08-39-41.csv');

fin = 80;
doublestime = str2double(data.Var1(2:fin));
doubles05 = str2double(data.Var6(2:fin));         %EXTREMEBLY dumb, the 0.5 ounts column is read in as strings unlike the others
cnt10 = data.Var7(2:fin);
cnt25 = data.Var8(2:fin);
cnt50 = data.Var9(2:fin);
cnt75 = data.Var10(2:fin);
cnt100 = data.Var11(2:fin);

step = 0.25; max = 8;
Np = max/step + 1;
particles = 0:step:max;
times = doublestime;
counts = zeros(length(times), length(particles));

for i = 1:length(particles)
    if(particles(i) == 0.5)
        counts(:,i) = doubles05;
    elseif(particles(i) == 1.0)
        counts(:,i) = cnt10;
    elseif(particles(i) == 2.5)
        counts(:,i) = cnt25;
    elseif(particles(i) == 5.0)
        counts(:,i) = cnt50;
    elseif(particles(i) == 7.5)
        counts(:,i) = cnt75;
    elseif(particles(i) == 10)
        counts(:,i) = cnt100;
    end
    
end

figure;
h = bar3(counts, 1);
remove_empty_bars(h);
colormap(flipud(parula(30)));
box on;

ylabel("Time (s)");
xlabel("Particle size (micron)");
zlabel("Raw counts");

% Change the x and y axis tick labels
ax = gca;
ax.XTickLabelMode = 'manual';
ax.XTickMode = 'manual';
xticks([3 5 11 21 31]);
xticklabels({'0.5', '1.0', '2.5', '5.0', '7.5'});
xtickangle(90);
pbaspect([2 3 1]);


% thanks to https://stackoverflow.com/a/2050658
% improves bar plot clarity by erasing the zero value bars
function remove_empty_bars(hBars)
  for iSeries = 1:numel(hBars)
    zData = get(hBars(iSeries), 'ZData');  % Get the z data
    index = logical(kron(zData(2:6:end, 2) == 0, ones(6, 1)));  % Find empty bars
    zData(index, :) = nan;                 % Set the z data for empty bars to nan
    set(hBars(iSeries), 'ZData', zData);   % Update the graphics objects
  end
end