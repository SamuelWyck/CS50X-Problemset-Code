#include <stdio.h>

int main(void)
{
    char *s = "HI!";
    printf("%c", *s);
    printf("%c", *(s + 1));
    printf("%c\n", *(s + 2));
}



/*
int main(void)
{
    int n = 50;
    int *p = &n;
    printf("%i\n", p);
}
*/
