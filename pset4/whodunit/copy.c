/* Copies a BMP piece by piece, just because.  */
#include <stdio.h>
#include <stdlib.h>
#include "bmp.h"

int main(int argc, char *argv[])
{
    if (argc != 3)      // ensure proper usage
    {
        fprintf(stderr, "Usage: ./copy infile outfile\n");
        return 1;
    }
    
    char *infile = argv[1];     // remember filenames
    char *outfile = argv[2];

    FILE *inptr = fopen(infile, "r");        // open input file 
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    FILE *outptr = fopen(outfile, "w");     // open output file
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    BITMAPFILEHEADER bf;            // read infile's BITMAPFILEHEADER
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    BITMAPINFOHEADER bi;            
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
                                                        // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || 
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);       // write outfile's BITMAPFILEHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);       // write outfile's BITMAPINFOHEADER

    int padding =  (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;      // determine padding for scanlines

    for (int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)      // iterate over infile's scanlines
    {
        for (int j = 0; j < bi.biWidth; j++)        // iterate over pixels in scanline
        {
            RGBTRIPLE triple;       // temporary storage

            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);        // read RGB triple from infile
            fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);      // write RGB triple to outfile
        }

        fseek(inptr, padding, SEEK_CUR);        // skip over padding, if any

        for (int k = 0; k < padding; k++)       // then add it back (to demonstrate how)
            fputc(0x00, outptr);
    }
    fclose(inptr);      // close infile
    fclose(outptr);     // close outfile

    return 0;       // success
}
