cython --embed -3 main.py
#gcc -Os -I /usr/include/python3.10 -o out main.c -lpython3.10 -lpthread -lm -lutil -ldl -s
gcc -Os -I /usr/include/python3.10 -o out main.c -lpython3.10 -lpthread -lm -lutil -ldl -s
#gcc -Os -I /usr/include/python3.10 -o out.so main.c -lpython3.10 -lpthread -lm -lutil -ldl -shared -fPIC -s
#gcc -Os -I /usr/include/python3.10 -o out.o main.c -lpython3.10 -lpthread -lm -lutil -ldl -c
