CC=gcc
CFLAGS=-Wall -O2
SRC=main.c \
    collector/sys_info.c \
    collector/os_info.c \
    collector/net_info.c \
    collector/geo_info.c \
    collector/utils.c
OBJ=$(SRC:.c=.o)
BIN=mycollector

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(OBJ) $(BIN)
