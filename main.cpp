#include <iostream>
#include <dirent.h>
#include <string>
#include <cerrno>
#include <cstring>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <time.h>

void printFileProperties(const std::string& path, const struct stat& stats) {
    std::cout << "\nFile: " << path;
    // File size
    std::cout << "\nSize: " << stats.st_size << " bytes";
    // File permissions
    std::cout << "\nPermissions: ";
    std::cout << ((stats.st_mode & S_IRUSR) ? "r" : "-");
    std::cout << ((stats.st_mode & S_IWUSR) ? "w" : "-");
    std::cout << ((stats.st_mode & S_IXUSR) ? "x" : "-");
    // Timestamps
    char timeStr[100];
    struct tm* timeinfo;
    timeinfo = localtime(&stats.st_mtime);
    strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", timeinfo);
    std::cout << "\nLast modified: " << timeStr;
    timeinfo = localtime(&stats.st_ctime);
    strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", timeinfo);
    std::cout << "\nCreated: " << timeStr << "\n";
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <directory_path>" << std::endl;
        return 1;
    }

    DIR* dir = opendir(argv[1]);
    if (dir == nullptr) {
        std::cerr << "Error opening directory: " << strerror(errno) << std::endl;
        return 1;
    }

    struct dirent* entry;
    struct stat stats;
    std::string basePath(argv[1]);
    std::string newDir = basePath + "/new_folder";

    // Create the new folder
    if (mkdir(newDir.c_str(), 0755) != 0) {
        std::cerr << "Error creating directory: " << strerror(errno) << std::endl;
        closedir(dir);
        return 1;
    }

    while ((entry = readdir(dir)) != nullptr) {
        std::string fullPath = basePath + "/" + entry->d_name;
        if (entry->d_name != std::string(".") && entry->d_name != std::string("..")) {
            // Move files to the new folder
            std::string newFilePath = newDir + "/" + entry->d_name;
            if (rename(fullPath.c_str(), newFilePath.c_str()) != 0) {
                std::cerr << "Error moving file to " << newFilePath << ": " 
                         << strerror(errno) << std::endl;
            }
        }
        if (stat(newDir.c_str(), &stats) == 0) {
            printFileProperties(entry->d_name, stats);
        }
    }

    closedir(dir);
    return 0;
}
