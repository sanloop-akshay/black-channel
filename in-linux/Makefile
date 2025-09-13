CC = gcc
CFLAGS = -Wall -Wextra -Icollector -Itasks -Imonitor
LIBS = -lcurl

OBJS_MAIN = main.o \
            collector/sys_info.o collector/os_info.o collector/net_info.o \
            collector/geo_info.o collector/utils.o \
            tasks/mailer.o monitor/listener.o

OBJS_TRIGGER = monitor/trigger.o \
               collector/sys_info.o collector/os_info.o collector/net_info.o \
               collector/geo_info.o collector/utils.o \
               tasks/mailer.o

all: black-channel trigger

black-channel: $(OBJS_MAIN)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

trigger: $(OBJS_TRIGGER)
	$(CC) $(CFLAGS) -o $@ $^ $(LIBS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f *.o collector/*.o tasks/*.o monitor/*.o black-channel trigger
