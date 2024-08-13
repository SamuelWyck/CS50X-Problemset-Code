#include <cs50.h>
#include <stdio.h>
#include <string.h>

int player_score(int length, string word);

int main(void)
{
    string player1_word = get_string("Player 1: ");
    string player2_word = get_string("Player 2: ");

    int player1_score = player_score(strlen(player1_word), player1_word);
    int player2_score = player_score(strlen(player2_word), player2_word);

    if (player1_score > player2_score)
    {
        printf("Player 1 wins!\n");
    }
    else if (player1_score < player2_score)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int player_score(int length, string word)
{
    int score = 0;
    for (int i = 0; i < length; i++)
    {
        if (word[i] == 'A' || word[i] == 'a')
        {
            score = score + 1;
        }
        else if (word[i] == 'B' || word[i] == 'b')
        {
            score = score + 3;
        }
        else if (word[i] == 'C' || word[i] == 'c')
        {
            score = score + 3;
        }
        else if (word[i] == 'D' || word[i] == 'd')
        {
            score = score + 2;
        }
        else if (word[i] == 'E' || word[i] == 'e')
        {
            score = score + 1;
        }
        else if (word[i] == 'F' || word[i] == 'f')
        {
            score = score + 4;
        }
        else if (word[i] == 'G' || word[i] == 'g')
        {
            score = score + 2;
        }
        else if (word[i] == 'H' || word[i] == 'h')
        {
            score = score + 4;
        }
        else if (word[i] == 'I' || word[i] == 'i')
        {
            score = score + 1;
        }
        else if (word[i] == 'J' || word[i] == 'j')
        {
            score = score + 8;
        }
        else if (word[i] == 'K' || word[i] == 'k')
        {
            score = score + 5;
        }
        else if (word[i] == 'L' || word[i] == 'l')
        {
            score = score + 1;
        }
        else if (word[i] == 'M' || word[i] == 'm')
        {
            score = score + 3;
        }
        else if (word[i] == 'N' || word[i] == 'n')
        {
            score = score + 1;
        }
        else if (word[i] == 'O' || word[i] == 'o')
        {
            score = score + 1;
        }
        else if (word[i] == 'P' || word[i] == 'p')
        {
            score = score + 3;
        }
        else if (word[i] == 'Q' || word[i] == 'q')
        {
            score = score + 10;
        }
        else if (word[i] == 'R' || word[i] == 'r')
        {
            score = score + 1;
        }
        else if (word[i] == 'S' || word[i] == 's')
        {
            score = score + 1;
        }
        else if (word[i] == 'T' || word[i] == 't')
        {
            score = score + 1;
        }
        else if (word[i] == 'U' || word[i] == 'u')
        {
            score = score + 1;
        }
        else if (word[i] == 'V' || word[i] == 'v')
        {
            score = score + 4;
        }
        else if (word[i] == 'W' || word[i] == 'w')
        {
            score = score + 4;
        }
        else if (word[i] == 'X' || word[i] == 'x')
        {
            score = score + 8;
        }
        else if (word[i] == 'Y' || word[i] == 'y')
        {
            score = score + 4;
        }
        else if (word[i] == 'Z' || word[i] == 'z')
        {
            score = score + 10;
        }
    }
    return score;
}
