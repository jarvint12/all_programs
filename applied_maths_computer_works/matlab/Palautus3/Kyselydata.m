load('Kyselydata.mat', 'predictors')
%predictors = työaika
%responses = maksuhalukkuus
model = fitlm(predictors, responses, 'linear');
figure
hold on
plot(predictors, responses, 'rx')
plot(predictors, predict(model, predictors))
hold on