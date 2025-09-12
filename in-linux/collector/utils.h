#ifndef UTILS_H
#define UTILS_H

char *run_cmd(const char *cmd);
char *try_cmd_or(const char *cmd, const char *fallback);
void trim(char *s);

#endif
