#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include "../collector/sys_info.h"
#include "../tasks/mailer.h"

#define OFFLINE_DIR "offline_reports"

static void send_offline_reports(const char *recipient) {
    DIR *dir = opendir(OFFLINE_DIR);
    if (!dir) {
        printf("[-] No offline_reports directory, skipping...\n");
        return;
    }

    struct dirent *entry;
    int sent_any = 0;

    while ((entry = readdir(dir)) != NULL) {
        if (entry->d_type == DT_REG) {
            char filepath[512];
            snprintf(filepath, sizeof(filepath), "%s/%s", OFFLINE_DIR, entry->d_name);

            FILE *fp = fopen(filepath, "r");
            if (!fp) continue;

            fseek(fp, 0, SEEK_END);
            long len = ftell(fp);
            rewind(fp);

            char *buf = malloc(len + 1);
            if (!buf) {
                fclose(fp);
                continue;
            }

            fread(buf, 1, len, fp);
            buf[len] = '\0';
            fclose(fp);

            if (send_mail(recipient, "Buffered System Report", buf) == 0) {
                printf("[+] Sent buffered report: %s\n", filepath);
                remove(filepath);
                sent_any = 1;
            } else {
                printf("[-] Failed to send buffered report: %s\n", filepath);
            }
            free(buf);
        }
    }
    closedir(dir);

    if (!sent_any) {
        printf("[*] No buffered reports found.\n");
    }
}

int main(void) {
    const char *recipient = getenv("EMAIL_RECEIVER");
    if (!recipient || strlen(recipient) == 0) {
        fprintf(stderr, "[-] EMAIL_RECEIVER not set in environment.\n");
        return 1;
    }

    send_offline_reports(recipient);

    DIR *dir = opendir(OFFLINE_DIR);
    int empty = 1;
    if (dir) {
        struct dirent *entry;
        while ((entry = readdir(dir)) != NULL) {
            if (entry->d_type == DT_REG) {
                empty = 0;
                break;
            }
        }
        closedir(dir);
    }

    if (empty) {
        char *report = collect_sys_info();
        if (!report) {
            fprintf(stderr, "[-] Failed to collect system info\n");
            return 1;
        }

        if (send_mail(recipient, "System Report", report) == 0) {
            printf("[+] Fresh system report sent successfully!\n");
        } else {
            printf("[-] Failed to send fresh system report.\n");
        }

        free(report);
    }

    return 0;
}
