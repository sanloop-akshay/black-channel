#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include "mailer.h"

struct upload_status {
    const char *data;
    size_t bytes_read;
};

static size_t payload_source(void *ptr, size_t size, size_t nmemb, void *userp) {
    struct upload_status *upload = (struct upload_status *)userp;
    size_t max = size * nmemb;

    if (!upload->data || upload->data[upload->bytes_read] == '\0') {
        return 0; 
    }

    size_t len = strlen(upload->data + upload->bytes_read);
    if (len > max) len = max;

    memcpy(ptr, upload->data + upload->bytes_read, len);
    upload->bytes_read += len;

    return len;
}

int send_mail(const char *to, const char *subject, const char *body) {
    CURL *curl;
    CURLcode res = CURLE_OK;
    struct curl_slist *recipients = NULL;

    const char *email_host = getenv("EMAIL_HOST");
    const char *app_password = getenv("APP_PASSWORD");
    if (!email_host || !app_password) {
        fprintf(stderr, "Error: EMAIL_HOST or APP_PASSWORD not set in environment\n");
        return 1;
    }

    char payload[8192];
    snprintf(payload, sizeof(payload),
             "To: %s\r\n"
             "From: %s\r\n"
             "Subject: %s\r\n"
             "\r\n"
             "%s\r\n",
             to,
             email_host,
             subject,
             body);

    struct upload_status upload_ctx;
    upload_ctx.data = payload;
    upload_ctx.bytes_read = 0;

    curl = curl_easy_init();
    if (!curl) return 1;

    curl_easy_setopt(curl, CURLOPT_USERNAME, email_host);
    curl_easy_setopt(curl, CURLOPT_PASSWORD, app_password);
    curl_easy_setopt(curl, CURLOPT_URL, "smtp://smtp.gmail.com:587");
    curl_easy_setopt(curl, CURLOPT_USE_SSL, (long)CURLUSESSL_ALL);
    curl_easy_setopt(curl, CURLOPT_MAIL_FROM, email_host);
    recipients = curl_slist_append(recipients, to);
    curl_easy_setopt(curl, CURLOPT_MAIL_RCPT, recipients);

    curl_easy_setopt(curl, CURLOPT_READFUNCTION, payload_source);
    curl_easy_setopt(curl, CURLOPT_READDATA, &upload_ctx);
    curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        fprintf(stderr, "Email failed: %s\n", curl_easy_strerror(res));
    }

    curl_slist_free_all(recipients);
    curl_easy_cleanup(curl);

    return (int)res;
}
