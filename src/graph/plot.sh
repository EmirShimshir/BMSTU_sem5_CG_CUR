#!/opt/homebrew/bin/gnuplot -persist

reset

set terminal svg size 1280, 720 font "Helvetica,18"
set output 'plot1.svg'
set size ratio 0.56
set pointsize 0.9

set key right bottom
set xlabel "Кол-во полигонов, шт."
set ylabel "Время, мс"
set grid

f(x) = a*x + b
fit f(x) 'data1.txt' via a,b
g(x) = c*x + d
fit g(x) 'data2.txt' via c,d

plot f(x) title 'Модифицированный алгоритм Варнока', "./data1.txt" pt 9 title '', \
     g(x) title 'Классический алгоритм Варнока', "./data2.txt" pt 10 title ''
