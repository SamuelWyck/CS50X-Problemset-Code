#include <stdio.h>
#include <cs50.h>

void meow(int n);

int main(void)
{
    meow(3);
}

void meow(int n)
{
    for (int i = n ; i > 0; i = i - 1)
    {
        printf("meow\n");
    }
}
