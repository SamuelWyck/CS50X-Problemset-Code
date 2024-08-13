#include <stdio.h>
#include <cs50.h>

const int number_scores = 3;

int main(void)
{
    int scores[number_scores];

    for (int i = 0; i < number_scores; i++)
    {
        scores[i] = get_int("Score: ");
    }

    printf("Average: %f\n", (scores[0] + scores[1] + scores[2]) / (float) number_scores);
}
