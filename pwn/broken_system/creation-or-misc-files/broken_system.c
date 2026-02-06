#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#include <sys/prctl.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <sys/syscall.h>
#include <linux/audit.h>

#define LONESHA256_STATIC
#include "sha2.h"

void printhex(unsigned char* x, unsigned int len) {
    for (unsigned int i=0 ; i<len ; i++) {
        printf("%02x", x[i]);
    }
}

unsigned int hextobytes(unsigned char* hex, unsigned char* out) {
    unsigned int len = strlen(hex);
    for (int i=0 ; i<len ; i+=2) {
        if (sscanf(hex+i, "%2hhx", out+(i/2)) < 1) {
            puts("Invalid hex!");
            exit(1);
        }
    }
    return len/2;
}

void recovery_console() {
    FILE* fp = fopen("/dev/urandom", "r");
    if (fp == NULL) {
        perror("fopen(/dev/urandom)");
        exit(1);
    }
    unsigned char password[0x20];
    fread(password, sizeof(password), 1, fp);
    fclose(fp);
    unsigned char hash[0x20];
    sha256(&hash, &password, sizeof(password));
    printf("Key: ");
    printhex(hash, sizeof(hash));
    printf("\nWelcome admin, please enter your OTP\n> ");
    unsigned char otphex[0x40];
    unsigned char otp[0x20];
    gets(otphex);
    if (hextobytes(otphex, otp) != sizeof(otp) || memcmp(otp, password, sizeof(password))) {
        puts("Access denied!");
        exit(1);
    }
    puts("Access granted!");
    if (system("recovery_console")) {       // NOTE: this command intentionally doesn't exist, and is supposed to fail
        puts("[!] Console not implemented!");
        load_seccomp();
        puts("[!] Warning! System is critically damaged!");
        puts("[!] Shutting down...");
    }
}

struct sock_filter sock_filter[] = {
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, arch)),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, AUDIT_ARCH_X86_64, 0, 6),
  BPF_STMT(BPF_LD | BPF_W | BPF_ABS, offsetof(struct seccomp_data, nr)),
  BPF_JUMP(BPF_JMP | BPF_JGE | BPF_K, 0x40000000 , 0, 1),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, 0xffffffff , 0, 3),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_execve, 2, 0),
  BPF_JUMP(BPF_JMP | BPF_JEQ | BPF_K, __NR_execveat, 1, 0),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_ALLOW),
  BPF_STMT(BPF_RET | BPF_K, SECCOMP_RET_KILL_PROCESS),
};

struct sock_fprog prog = {
  .len = sizeof(sock_filter) / sizeof(sock_filter[0]),
  .filter = sock_filter,
};

void load_seccomp() {
  if(prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) < 0) {
    perror("prctl(PR_SET_NO_NEW_PRIVS)");
    exit(EXIT_FAILURE);
  }
  if(syscall(__NR_seccomp, SECCOMP_SET_MODE_FILTER, 0, &prog) < 0) {
    perror("seccomp(SECCOMP_SET_MODE_FILTER)");
    exit(EXIT_FAILURE);
  }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    char user[0x20] = {0};

    puts("[!] Emergency console login:");
    printf("Enter username: ");
    user[read(0, user, sizeof(user)) - 1] = 0;

    if (strcmp(user, "admin") == 0)
        recovery_console();
    else
        puts("Access denied!");
    return 0;
}