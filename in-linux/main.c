#include <stdio.h>
#include <stdlib.h>
#include "collector/sys_info.h"

int main(void) {
    char *report = collect_sys_info();
    if (report) {
        printf("%s\n", report);
        free(report);
    }
    return 0;
}
