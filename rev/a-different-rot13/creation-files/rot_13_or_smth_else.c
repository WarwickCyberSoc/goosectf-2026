#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BYTE_BITS 7
#define ROT_NUMBER (13 - BYTE_BITS)

char left_rotate(char n, unsigned char d)
{
    unsigned char masked = n & 0x7F;
    unsigned char rotated = ((masked << d) | (masked >> (BYTE_BITS - d))) & 0x7F;   
    return (char)rotated;
}

int main()
{
    FILE* fp = fopen("flag.txt", "r");
    if (fp == NULL) {
        printf("Flag file not found");
        exit(1);
    }

    char flag[0x100];
    fgets(flag, sizeof(flag), fp);

    for (int i = 0; i < strlen(flag); i++)
    {
        flag[i] = left_rotate(flag[i], ROT_NUMBER);
    }

    printf("%s", flag);

    return 0;
}