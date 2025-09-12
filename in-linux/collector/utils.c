#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "utils.h"

#define BUF_SIZE 4096

void trim(char *s) {
    if (!s) return;
    char *p = s;
    while (*p && isspace((unsigned char)*p)) p++;
    if (p != s) memmove(s, p, strlen(p)+1);
    size_t len = strlen(s);
    while (len > 0 && isspace((unsigned char)s[len-1])) s[--len] = '\0';
}

char *run_cmd(const char *cmd) {
    if (!cmd) return NULL;
    FILE *fp = popen(cmd, "r");
    if (!fp) return NULL;
    size_t cap = BUF_SIZE;
    char *out = malloc(cap);
    if (!out) { pclose(fp); return NULL; }
    out[0] = '\0';
    size_t len = 0;
    while (fgets(out + len, (int)(cap - len), fp) != NULL) {
        len = strlen(out);
        if (cap - len < 256) {
            cap *= 2;
            char *tmp = realloc(out, cap);
            if (!tmp) break;
            out = tmp;
        }
    }
    pclose(fp);
    trim(out);
    return out;
}

char *try_cmd_or(const char *cmd, const char *fallback) {
    char *r = run_cmd(cmd);
    if (!r || r[0] == '\0') {
        free(r);
        return strdup(fallback ? fallback : "N/A");
    }
    return r;
}
