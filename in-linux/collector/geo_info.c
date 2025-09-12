#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "geo_info.h"
#include "utils.h"

char *get_public_ip() {
    char *r = run_cmd("curl -s --max-time 5 https://ipinfo.io/ip 2>/dev/null");
    if (!r || r[0] == '\0') {
        free(r);
        r = run_cmd("curl -s --max-time 5 https://icanhazip.com 2>/dev/null");
    }
    if (!r || r[0] == '\0') {
        free(r);
        return strdup("N/A");
    }
    return r;
}

char *get_geolocation() {
    char *parsed = run_cmd("curl -s --max-time 6 https://ipinfo.io/json 2>/dev/null | jq -r '.city, .region, .country, .loc' | paste -s -d ',' -");
    if (!parsed || parsed[0]=='\0') {
        free(parsed);
        return strdup("N/A (no internet or parse failed)");
    }
    return parsed;
}
