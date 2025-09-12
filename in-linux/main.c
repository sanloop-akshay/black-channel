#include <stdio.h>
#include <stdlib.h>
#include "collector/sys_info.h"
#include "tasks/mailer.h"

int main(void) {
    char *report = collect_sys_info();
    if (report) {
        printf("%s\n", report);

        const char *recipient = "akshaypiranavb@gmail.com";
        if (send_mail(recipient, "System Report", report) == 0) {
            printf("Email sent successfully!\n");
        } else {
            printf("Failed to send email.\n");
        }

        free(report);
    }
    return 0;
}
