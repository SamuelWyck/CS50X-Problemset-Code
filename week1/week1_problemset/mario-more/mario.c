#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_pyramid(int height);

int main(void)
{
    print_pyramid(get_height());
}

int get_height(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    return height;
}

void print_pyramid(int height)
{
    int brick = 1;
    int space = height - 1;
    for (int i = height; i > 0; i = i - 1)
    {
        for (int k = space; k > 0; k = k - 1)
        {
            printf(" ");
        }
        for (int j = brick; j > 0; j = j - 1)
        {
            printf("#");
        }
        printf("  ");
        for (int h = brick; h > 0; h = h - 1)
        {
            printf("#");
        }
        space = space - 1;
        brick = brick + 1;
        printf("\n");
    }
}

