#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int size;
    do
    {
        size = get_int("Size: ");
    }
    while (size < 1);

    for (int i = 0; i < size; i = i + 1)
    {
        for (int j = 0; j < size; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}
