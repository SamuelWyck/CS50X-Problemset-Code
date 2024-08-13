#include <stdio.h>
#include <cs50.h>

int number_coin(int n);

int main(void)
{
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);

    printf("%i\n", number_coin(change));
}

int number_coin(int cents)
{
    int coins = 0;
    while (true)
    {
        if ((cents - 25) >= 0)
        {
            coins = coins + 1;
            cents = cents - 25;
        }
        else if ((cents - 10) >= 0)
        {
            coins = coins + 1;
            cents = cents - 10;
        }
        else if ((cents - 5) >= 0)
        {
            coins = coins + 1;
            cents = cents - 5;
        }
        else if ((cents - 1) >= 0)
        {
            coins = coins + 1;
            cents = cents - 1;
        }
        else
        {
            break;
        }
    }
    return coins;
}
