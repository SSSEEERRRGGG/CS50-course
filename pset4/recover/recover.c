#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char* argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "lack of forensic image .\n");
        return 1;
    }
    FILE* inptr = fopen(argv[1], "r");      // open memory card file
    if (inptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create file .\n");
        return 2;
    }
    FILE* outptr = NULL;

    typedef uint8_t  BYTE;      // create 512 byte buffer array
    BYTE buffer[512];

    BYTE firstfour[4];      // create array for first four bytes of the buffer

    BYTE jpgsig[4] = {0xff, 0xd8, 0xff, 0xe0};          // the first 4 bytes of a jpg file (i.e. jpg signature)
                                                        // the last four bits can range from 0-f and are hardcoded as zeros here
    int jpgnumber = 0;              // keep track of jpg numbers for jpg filenames
    char jpgfilename[8];
    
    while (fread(&buffer, sizeof(buffer), 1, inptr) > 0) // read a buffer from card.raw until EOF
    {
     	for (int i = 0; i < 4; i++)         // load first three bytes of the buffer into firstfour
	    {
	        firstfour[i] = buffer[i];
	    }
    	firstfour[3] = (firstfour[3] >> 4) << 4;        // hardcode zeros into last four bits of fourth byte in firstfour
	
        if (memcmp(firstfour, jpgsig, sizeof(jpgsig)) == 0)     // if jpg signature is found
        {
            // a jpg is not open yet
            if (outptr == NULL)
            {
                sprintf(jpgfilename, "%03d.jpg", jpgnumber);
                outptr = fopen(jpgfilename, "a");
                fwrite(&buffer, sizeof(buffer), 1, outptr);
            }
            else                // a jpg is already open
            {
                fclose(outptr);
                jpgnumber++;
                sprintf(jpgfilename, "%03d.jpg", jpgnumber);
                outptr = fopen(jpgfilename, "a");
                fwrite(&buffer, sizeof(buffer), 1, outptr);
            }
        }
        else
        {
            if (outptr != NULL)         // a jpg is already open
                fwrite(&buffer, sizeof(buffer), 1, outptr);
        }
    }
    fclose(inptr);      // close files and exit cleanly
    fclose(outptr);
    return 0;
}