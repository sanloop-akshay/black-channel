#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "net_info.h"
#include "utils.h"

char *get_ip_addresses() {
    return try_cmd_or("ip -4 -o addr show scope global 2>/dev/null | awk '{print $2\" -> \"$4}' | paste -s -d ',' -", "N/A");
}

char *get_default_route() {
    return try_cmd_or("ip route show default 2>/dev/null | awk 'NR==1{print $0}'", "N/A");
}

char *get_wireless_iface() {
    char *r = run_cmd("iw dev 2>/dev/null | awk '/Interface/ {print $2; exit}'");
    if (!r || r[0] == '\0') {
        free(r);
        r = run_cmd("ls /sys/class/net 2>/dev/null | tr '\\n' ' ' | awk '{for(i=1;i<=NF;i++) if ($i ~ /^wlan|^wl/) {print $i; exit}}'");
    }
    if (!r || r[0] == '\0') {
        free(r);
        return strdup("N/A");
    }
    return r;
}

char *get_wifi_ssid_auto(void) {
    char *r = run_cmd("iwgetid -r 2>/dev/null");
    if (!r || r[0] == '\0') {
        free(r);
        r = run_cmd("nmcli -t -f ACTIVE,SSID dev wifi 2>/dev/null | awk -F: '$1==\"yes\"{print $2; exit}'");
    }
    if (!r || r[0] == '\0') {
        free(r);
        return strdup("N/A");
    }
    return r;
}

char *get_wifi_details_auto(void) {
    char *iface = get_wireless_iface();
    if (!iface || strcmp(iface, "N/A")==0) return strdup("N/A");

    char cmd[256];
    snprintf(cmd, sizeof(cmd), "iw dev %s link 2>/dev/null | sed -n '1,5p' | paste -s -d ';' -", iface);
    char *r = run_cmd(cmd);
    if (!r || r[0] == '\0') {
        free(r);
        snprintf(cmd, sizeof(cmd), "iwconfig %s 2>/dev/null | sed -n '1,5p' | paste -s -d ';' -", iface);
        r = run_cmd(cmd);
    }
    if (!r || r[0] == '\0') {
        free(r);
        free(iface);
        return strdup("N/A");
    }
    free(iface);
    return r;
}

char *get_mac_auto(void) {
    char *iface = get_wireless_iface();
    if (!iface || strcmp(iface, "N/A")==0) return strdup("N/A");

    char cmd[200];
    snprintf(cmd, sizeof(cmd), "cat /sys/class/net/%s/address 2>/dev/null", iface);
    char *r = try_cmd_or(cmd, "N/A");
    free(iface);
    return r;
}
