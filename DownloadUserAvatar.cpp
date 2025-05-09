#include <curl/curl.h>
#include <iostream>

// response header data
struct HeaderData {
    std::string data;
};

// Callback function: collect response header data
size_t header_callback(char* buffer, size_t size, size_t nitems, void* userdata) {
    size_t total_size = size * nitems;
    HeaderData* headerData = static_cast<HeaderData*>(userdata);
    headerData->data.append(buffer, total_size);
    return total_size;
}

int DownloadUserAvatar(void* handler, const char* const uid_str, const char* const dest_filename)
{
    const std::string url_640 = std::string("http://q1.qlogo.cn/g?b=qq&nk=") + uid_str + "&s=640"; // the url to download avatars
    const std::string url_140 = std::string("http://q1.qlogo.cn/g?b=qq&nk=") + uid_str + "&s=140";
    CURL* const curl = curl_easy_init();
    if (!curl) {
        std::cerr << "DownloadUserAvatar curl_easy_init() failed" << std::endl;
        return false;
    }
    FILE* fp = fopen(dest_filename, "wb");
    if (!fp) {
        std::cerr << "DownloadUserAvatar open dest file failed, path: " << dest_filename << std::endl;
        curl_easy_cleanup(curl);
        return false;
    }
    HeaderData headerData;
    curl_easy_setopt(curl, CURLOPT_URL, url_640.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, fwrite);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
    curl_easy_setopt(curl, CURLOPT_HEADERFUNCTION, header_callback);
    curl_easy_setopt(curl, CURLOPT_HEADERDATA, &headerData);
    CURLcode res = curl_easy_perform(curl);
    if (res == CURLE_OK) {
        const size_t pos = headerData.data.find("Cache-Control:");
        if (pos != std::string::npos) {
            size_t endPos = headerData.data.find("\r\n", pos);
            if (headerData.data.substr(pos, endPos - pos).find("no-cache") != std::string::npos) {
                std::cerr << uid_str << " 640px avatar unavailable, using 140px instead" << std::endl;
                fclose(fp);
                fp = fopen(dest_filename, "wb");
                if (!fp) {
                    std::cerr << "Failed to open file for 140px avatar." << std::endl;
                    curl_easy_cleanup(curl);
                    return false;
                }
                curl_easy_reset(curl);
                curl_easy_setopt(curl, CURLOPT_URL, url_140.c_str());
                curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, fwrite);
                curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
                res = curl_easy_perform(curl);
            }
        }
    }
    if (res != CURLE_OK) {
        std::cerr << "DownloadUserAvatar curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
    }
    headerData.data.clear();
    curl_easy_cleanup(curl);
    fclose(fp);
    return res == CURLE_OK;
}

int main()
{
    void* handler;
    DownloadUserAvatar(handler, "2295824927", "1.png");
    return 0;
}
