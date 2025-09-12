#include "sys_info.h"
#include "os_info.h"
#include "net_info.h"
#include "geo_info.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static InfoCollector collectors[] = {
    {"Hostname",        get_hostname},
    {"Distro",          get_distro},
    {"Kernel & Arch",   get_uname},
    {"Uptime",          get_uptime},
    {"Local IPs",       get_ip_addresses},
    {"Default Route",   get_default_route},
    {"Wireless IFACE",  get_wireless_iface},
    {"Wi-Fi SSID",      get_wifi_ssid_auto},
    {"Wi-Fi Details",   get_wifi_details_auto},
    {"Wi-Fi MAC",       get_mac_auto},
    {"Public IP",       get_public_ip},
    {"Geo (IP based)",  get_geolocation}
};

char* collect_sys_info(void) {
    size_t cap = 4096, len = 0;
    char *out = malloc(cap);
    out[0] = '\0';

    len += snprintf(out + len, cap - len, "=== System & Network Info Collector (Linux) ===\n\n");

    for (size_t i = 0; i < sizeof(collectors)/sizeof(collectors[0]); i++) {
        char *val = collectors[i].collector();
        if (!val) val = strdup("N/A");

        size_t need = strlen(val) + 64;
        if (len + need >= cap) {
            cap *= 2;
            out = realloc(out, cap);
        }

        len += snprintf(out + len, cap - len, "%-16s: %s\n", collectors[i].label, val);
        free(val);
    }
    return out;
}
