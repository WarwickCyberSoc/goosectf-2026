#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

int fd = -1;

unsigned long readline(char* buf, size_t max) {
    fgets(buf, max, stdin);
    size_t len = strcspn(buf, "\n");
    if (buf[len] == '\n') {
        buf[len] = 0;
    }
    return len;
}

void open_novel() {
    if (fd != -1) {
        puts("You need to finish what you started!");
        return;
    }
    char novel[0x80];
    printf("Novel: ");
    size_t len = readline(novel, sizeof(novel));

    char path[0x90];
    memset(path, 0, sizeof(path));
    strcat(path, "novels/");

    //strcat(path, novel)

    // Remove "../" to stop pesky directory traversal!
    int i = 0;
    int j = strlen(path);
    while (i < len) {
        if (strncmp(novel+i, "../", 3) == 0) {
            i += 3;
        } else {
            path[j++] = novel[i++];
        }
    }
    path[j] = 0;

    if (strstr(path, "flag")) {
        puts("This novel is reserved for only true hackers!");
        exit(1);
    }
    fd = open(path, O_RDWR);
    if (fd > 0) {
        puts("Enjoy your new novel!");
    } else {
        perror("open");
        exit(1);
    }
}

void _read_novel(size_t offset, size_t size) {
    char* buf = malloc(size);
    if (buf == NULL) {
        perror("malloc");
        exit(1);
    }
    pread(fd, buf, size, offset);
    puts(buf);
    free(buf);
}

void read_novel() {
    if (fd == -1) {
        puts("What novel were you planning to read!");
        return;
    }
    printf("Enter offset and size: ");
    size_t offset, size;
    int in = scanf("%zu %zu", &offset, &size);
    getchar();
    if (in < 2)
        return;
    
    _read_novel(offset, size);
}

void edit_novel() {
    if (fd == -1) {
        puts("What novel were you planning to edit!");
        return;
    }
    printf("Enter offset and size: ");
    size_t offset, size;
    int in = scanf("%zu %zu", &offset, &size);
    getchar();
    if (in < 2)
        return;

    char* buf = malloc(size);
    if (buf == NULL) {
        perror("malloc");
        exit(1);
    }

    puts("------ SNIPPET ------");
    _read_novel(offset, size);
    puts("---- END SNIPPET ----");

    printf("Enter edit: ");
    size = readline(buf, size);
    pwrite(fd, buf, size, offset);
    free(buf);
}

void publish_novel() {
    if (fd == -1) {
        puts("What novel were you planning to publish!");
        return;
    }
    close(fd);
    fd = -1;
    puts("Novel has been published!");
}

int menu() {
    puts("1. Open novel");
    puts("2. Read novel");
    puts("3. Edit novel");
    puts("4. Publish novel");
    puts("5. Clock out");
    printf("> ");
    int option;
    int in = scanf("%d", &option);
    getchar();
    if (in < 1)
        return -1;
    return option;
}

void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main() {
    setup();
    while (1) {
        switch (menu()) {
            case 1:
                open_novel();
                break;

            case 2:
                read_novel();
                break;

            case 3:
                edit_novel();
                break;
            
            case 4:
                publish_novel();
                break;

            case 5:
                return 0;

            default:
                puts("Invalid option!");
                break;
        }
    }
}