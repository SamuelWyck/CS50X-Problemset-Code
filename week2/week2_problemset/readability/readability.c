#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

string lower(string passage);
int count_letters(string passage);
int count_words(string passage);
int count_sentences(string passage);
int liau_index(int letters, int words, int sentences);

int main(void)
{
    string text = lower(get_string("Text: "));
    int number_letters = count_letters(text);
    int number_words = count_words(text);
    int number_sentences = count_sentences(text);
    int grade_level = liau_index(number_letters, number_words, number_sentences);
    if (grade_level < 0)
    {
        printf("Before Grade 1\n");
    }
    else if (grade_level >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade_level);
    }
}

string lower(string passage)
{
    for (int i = 0, length = strlen(passage); i < length; i++)
    {
        passage[i] = tolower(passage[i]);
    }
    return passage;
}

int count_letters(string passage)
{
    int letters = 0;
    for (int i = 0, length = strlen(passage); i < length; i++)
    {
        if (isalpha(passage[i]))
        {
            letters = letters + 1;
        }
    }
    return letters;
}

int count_words(string passage)
{
    int words = 0;
    for (int i = 0, length = strlen(passage); i < length; i++)
    {
        if (isblank(passage[i]))
        {
            words = words + 1;
        }
    }
    return (words + 1);
}

int count_sentences(string passage)
{
    int sentences = 0;
    for (int i = 0, length = strlen(passage); i < length; i++)
    {
        if (passage[i] == '.' || passage[i] == '?' || passage[i] == '!')
        {
            sentences = sentences + 1;
        }
    }
    return sentences;
}

int liau_index(int letters, int words, int sentences)
{
    float L = (((float) letters / (float) words) * 100.0);
    float S = (((float) sentences / (float) words) * 100.0);
    float index = (0.0588 * L) - (0.296 * S) - 15.8;
    index = rint(index);
    return index;
}
