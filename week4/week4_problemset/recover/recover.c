#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Useage: recover.c file.jpeg\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Cannot open file.\n");
        return 1;
    }

    uint8_t buffer[512];
    char picnum[9];
    int pic = -1;

    int file = 0;
    int file_counter = 0;

    while(fread(buffer, 1, 512, input) == 512)
    {

        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] == 0xe0 || buffer[3] == 0xe1 || buffer[3] == 0xe2 || buffer[3] == 0xe3 || buffer[3] == 0xe4 || buffer[3] == 0xe5 || buffer[3] == 0xe6 || buffer[3] == 0xe7 || buffer[3] == 0xe8 || buffer[3] == 0xe9 || buffer[3] == 0xea || buffer[3] == 0xeb || buffer[3] == 0xec || buffer[3] == 0xed || buffer[3] == 0xee || buffer[3] == 0xef))
        {
            pic += 1;
            if (pic < 10)
            {
                sprintf(picnum, "00%i.jpg", pic);
            }
            else if (pic >= 10)
            {
                sprintf(picnum, "0%i.jpg", pic);
            }

            FILE *picture = fopen(picnum, "a");
            fwrite(&buffer, sizeof(buffer), 1, picture);
            file += 1;
            fclose(picture);
        }

        else if(file - file_counter == 1)
        {
            if (pic < 10)
            {
                sprintf(picnum, "00%i.jpg", pic);
            }
            else if (pic >= 10)
            {
                sprintf(picnum, "0%i.jpg", pic);
            }
            FILE *picture = fopen(picnum, "a");
            fwrite(&buffer, sizeof(buffer), 1, picture);
            fclose(picture);
        }

        else if (file - file_counter == 2)
        {
            if (pic < 10)
            {
                sprintf(picnum, "00%i.jpg", pic);
            }
            else if (pic >= 10)
            {
                sprintf(picnum, "0%i.jpg", pic);
            }
            FILE *picture = fopen(picnum, "a");
            fwrite(&buffer, sizeof(buffer), 1, picture);
            file_counter += 1;
            fclose(picture);
        }
    }
    fclose(input);
    return 0;
}
