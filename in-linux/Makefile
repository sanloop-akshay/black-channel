CC = gcc
CFLAGS = -Wall -O2
BIN = start-watch

SRC = main.c \
      collector/sys_info.c \
      collector/os_info.c \
      collector/net_info.c \
      collector/geo_info.c \
      collector/utils.c \
      tasks/mailer.c

OBJ = $(SRC:.c=.o)

all: $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) -lcurl

clean:
	rm -f $(OBJ) $(BIN)
