#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    string s = get_string("Before: ");
    printf("After:  ");
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        printf("%c", toupper(s[i]));
    }
    printf("\n");
}
