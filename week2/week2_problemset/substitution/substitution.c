#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int check_alpha(string key);
int check_repeat(string key);
string lower(string passage);
void cipher(string key, string text);

int main(int argc, string argv[])
{
    if (argc != 2 || strlen(argv[1]) != 26 || check_alpha(argv[1]) != 26 || check_repeat(lower(argv[1])) != 26)
    {
        printf("You are made of stupid.\n");
        return 1;
    }
    string good_key = lower(argv[1]);
    string plain_text = get_string("plaintext:  ");
    cipher(good_key, plain_text);
}

int check_alpha(string key)
{
    int letter_check = 0;
    for (int i = 0, length = strlen(key); i < length; i++)
    {
        if (isalpha(key[i]))
        {
            letter_check = letter_check + 1;
        }
    }
    return letter_check;
}

int check_repeat(string key)
{
    int repeat_letters = 0;
    for (int i = 0, length = strlen(key); i < length; i++)
    {
        for (int j = 0; j < length; j++)
        {
            if (key[i] == key[j])
            {
                repeat_letters = repeat_letters + 1;
            }
        }
    }
    return repeat_letters;
}

string lower(string passage)
{
    for (int i = 0, length = strlen(passage); i < length; i++)
    {
        passage[i] = tolower(passage[i]);
    }
    return passage;
}

void cipher(string key, string text)
{
    char original_text[strlen(text) + 1];
    for (int i = 0; i < strlen(text) + 1; i++)
    {
        original_text[i] = 0;
    }

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        original_text[i] = text[i];
    }

    string lower_text = lower(text);

    char new_text[strlen(text) + 1];
    for (int i = 0; i < strlen(text) + 1; i++)
    {
        new_text[i] = 0;
    }

    string alphabet = "abcdefghijklmnopqrstuvwxyz";
    for (int i = 0, length = strlen(text); i < length; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            if (lower_text[i] == alphabet[j])
            {
                new_text[i] = key[j];
            }
            else if (!isalpha(lower_text[i]))
            {
                new_text[i] = lower_text[i];
            }
        }
    }

    char cipher_text[strlen(text) + 1];
    for (int i = 0; i < strlen(text) + 1; i++)
    {
        cipher_text[i] = 0;
    }

    for (int i = 0, length = strlen(text); i < length; i++)
    {
        if (isupper(original_text[i]))
        {
            cipher_text[i] = toupper(new_text[i]);
        }
        else
        {
            cipher_text[i] = new_text[i];
        }
    }

    //printf("%s\n", original_text);
    //printf("%s\n", lower_text);
    //printf("%s\n", new_text);
    printf("ciphertext: %s\n", cipher_text);
}
