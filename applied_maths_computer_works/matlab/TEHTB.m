load('Kyselydata')
model = fitlm(predictors, responses, 'linear');
x = [10:60]';

plot(x, predict(model,x));
hold on
plot(predictors, responses, 'o')

