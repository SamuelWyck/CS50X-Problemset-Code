#include "helpers.h"
#include <math.h>

int cap(int color);
int ClampMinRow(int row, int minrow);
int ClampMaxRow(int row, int maxrow);
int ClampMinCol(int col, int mincol);
int ClampMaxCol(int col, int maxcol);
RGBTRIPLE calcblur(int row, int col, int height, int width, RGBTRIPLE image[height][width]);


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = rint((image[i][j].rgbtGreen + image[i][j].rgbtRed + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = cap(rint(.393 * (float) image[i][j].rgbtRed + .769 * (float) image[i][j].rgbtGreen + .189 * (float) image[i][j].rgbtBlue));
            int sepiaGreen = cap(rint(.349 * (float) image[i][j].rgbtRed + .686 * (float) image[i][j].rgbtGreen + .168 * (float) image[i][j].rgbtBlue));
            int sepiaBlue = cap(rint(.272 * (float) image[i][j].rgbtRed + .534 * (float) image[i][j].rgbtGreen + .131 * (float) image[i][j].rgbtBlue));
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int pixel = 0;
        for (int j = 0, len = rint(width/2); j < len; j++)
        {
            RGBTRIPLE temp;
            temp = image[i][j];
            image[i][j] = image[i][width - 1 - pixel];
            image[i][width - 1 - pixel] = temp;
            pixel += 1;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j ++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            copy[row][col] = calcblur(row, col, height, width, image);
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j ++)
        {
            image[i][j] = copy[i][j];
        }
    }

    return;
}

int cap(int color)
{
    if (color > 255)
    {
        return 255;
    }
    return color;
}

RGBTRIPLE calcblur(int row, int col, int height, int width, RGBTRIPLE image[height][width])
{
    int StartBlurRow = ClampMinRow(row, 0);
    int EndBlurRow = ClampMaxRow(row, height - 1);
    int StartBlurCol = ClampMinCol(col, 0);
    int EndBlurCol = ClampMaxCol(col, width - 1);

    long SumRed = 0;
    long SumBlue = 0;
    long SumGreen = 0;
    int SumCount = 0;

    for (int blurRow = StartBlurRow; blurRow <= EndBlurRow; blurRow++)
    {
        for (int blurCol = StartBlurCol; blurCol <= EndBlurCol; blurCol++)
        {
            SumRed += image[blurRow][blurCol].rgbtRed;
            SumBlue += image[blurRow][blurCol].rgbtBlue;
            SumGreen += image[blurRow][blurCol].rgbtGreen;
            SumCount += 1;
        }
    }
    int AvgRed = rint((float) ((float) SumRed / (float) SumCount) + .01);
    int AvgBlue = rint((float) (((float) SumBlue / (float) SumCount)) + .01);
    int AvgGreen = rint((float) ((float) SumGreen / (float) SumCount) + .01);

    RGBTRIPLE pixel;
    pixel.rgbtRed = AvgRed;
    pixel.rgbtBlue = AvgBlue;
    pixel.rgbtGreen = AvgGreen;

    return pixel;
}

int ClampMinRow(int row, int minrow)
{
    if (row < minrow)
    {
        row = minrow;
        return row;
    }
    return fmax(0, row - 1);
}

int ClampMaxRow(int row, int maxrow)
{
    if (row > maxrow)
    {
        row = maxrow;
        return row;
    }
    return fmin(maxrow, row + 1);
}

int ClampMinCol(int col, int mincol)
{
    if (col < mincol)
    {
        col = mincol;
        return col;
    }
    return fmax(0, col - 1);
}

int ClampMaxCol(int col, int maxcol)
{
    if (col > maxcol)
    {
        col = maxcol;
        return col;
    }
    return fmin(maxcol, col + 1);
}
