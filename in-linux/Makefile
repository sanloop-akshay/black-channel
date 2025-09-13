CC=gcc
CFLAGS=-Wall -O2
LIBS=-lcurl

SRC=main.c \
    collector/sys_info.c collector/utils.c \
    collector/os_info.c collector/net_info.c collector/geo_info.c \
    tasks/mailer.c \
    monitor/listener.c

OBJ=$(SRC:.c=.o)

TARGET=black_channel

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $(OBJ) $(LIBS)

clean:
	rm -f $(OBJ) $(TARGET)
