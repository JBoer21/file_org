// Include necessary header files
#include <iostream>     // For input/output operations
#include <dirent.h>     // For directory handling functions
#include <string>       // For string operations
#include <cerrno>      // For error handling
#include <cstring>     // For string manipulation functions
#include <sys/stat.h>  // For file status functions
#include <sys/types.h> // For system types definitions
#include <unistd.h>    // For POSIX operating system API
#include <time.h>      // For time-related functions

// Function to print file properties, takes file path and stat structure as parameters
void printFileProperties(const std::string& path, const struct stat& stats) {
    std::cout << "\nFile: " << path;  // Print file name
    
    // Print file size in bytes
    std::cout << "\nSize: " << stats.st_size << " bytes";
    
    // Print file permissions (read/write/execute for user)
    std::cout << "\nPermissions: ";
    std::cout << ((stats.st_mode & S_IRUSR) ? "r" : "-");  // Read permission
    std::cout << ((stats.st_mode & S_IWUSR) ? "w" : "-");  // Write permission
    std::cout << ((stats.st_mode & S_IXUSR) ? "x" : "-");  // Execute permission
    
    // Create buffer for time string
    char timeStr[100];
    struct tm* timeinfo;
    
    // Convert and format last modification time
    timeinfo = localtime(&stats.st_mtime);
    strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", timeinfo);
    std::cout << "\nLast modified: " << timeStr;
    
    // Convert and format creation time
    timeinfo = localtime(&stats.st_ctime);
    strftime(timeStr, sizeof(timeStr), "%Y-%m-%d %H:%M:%S", timeinfo);
    std::cout << "\nCreated: " << timeStr << "\n";
}

int main(int argc, char* argv[]) {
    // Check if correct number of arguments provided
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <directory_path>" << std::endl;
        return 1;
    }

    // Open the directory
    DIR* dir = opendir(argv[1]);
    if (dir == nullptr) {
        std::cerr << "Error opening directory: " << strerror(errno) << std::endl;
        return 1;
    }

    // Declare variables for directory entry and file stats
    struct dirent* entry;
    struct stat stats;
    std::string basePath(argv[1]);
    std::string newDir = basePath + "/new_folder";

    // Create a new directory with permissions 0755
    if (mkdir(newDir.c_str(), 0755) != 0) {
        std::cerr << "Error creating directory: " << strerror(errno) << std::endl;
        closedir(dir);
        return 1;
    }

    // Read directory entries one by one
    while ((entry = readdir(dir)) != nullptr) {
        std::string fullPath = basePath + "/" + entry->d_name;
        
        // Skip current and parent directory entries
        if (entry->d_name != std::string(".") && entry->d_name != std::string("..")) {
            // Create new file path and move file to new directory
            std::string newFilePath = newDir + "/" + entry->d_name;
            if (rename(fullPath.c_str(), newFilePath.c_str()) != 0) {
                std::cerr << "Error moving file to " << newFilePath << ": " 
                         << strerror(errno) << std::endl;
            }
        }
        
        // Get and print file properties if stat succeeds
        if (stat(newDir.c_str(), &stats) == 0) {
            printFileProperties(entry->d_name, stats);
        }
    }

    // Close the directory and return
    closedir(dir);
    return 0;
}
