#include <stdlib.h>
#include <string.h>
#include "os_info.h"
#include "utils.h"

char *get_hostname() { return try_cmd_or("hostname", "N/A"); }

char *get_uname() { return try_cmd_or("uname -srmo 2>/dev/null", "N/A"); }

char *get_distro() {
    char *r = run_cmd("awk -F= '/^PRETTY_NAME/ {gsub(/\"/, \"\", $2); print $2; exit}' /etc/os-release 2>/dev/null");
    if (!r || r[0] == '\0') {
        free(r);
        r = run_cmd("lsb_release -ds 2>/dev/null");
    }
    if (!r || r[0] == '\0') {
        free(r);
        return strdup("N/A");
    }
    return r;
}

char *get_uptime() { return try_cmd_or("uptime -p 2>/dev/null", "N/A"); }
