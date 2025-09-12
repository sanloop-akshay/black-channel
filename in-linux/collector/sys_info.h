#ifndef SYS_INFO_H
#define SYS_INFO_H

typedef struct {
    const char *label;
    char* (*collector)(void);
} InfoCollector;

char* collect_sys_info(void);

#endif
