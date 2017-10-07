/**
 * fifteen.c
 *
 * Implements Game of Fifteen (generalized to d x d).
 * Usage: fifteen d
 *
 * whereby the board's dimensions are to be d x d,
 * where d must be in [DIM_MIN,DIM_MAX]
 *
 * Note that usleep is obsolete, but it offers more granularity than
 * sleep and is simpler to use than nanosleep; `man usleep` for more.
 */
#define _XOPEN_SOURCE 500

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define DIM_MIN 3       // constants
#define DIM_MAX 9

int board[DIM_MAX][DIM_MAX];        // board

int d;      // dimensions

void clear(void);       // prototypes
void greet(void);
void init(void);
void draw(void);
bool move(int tile);
bool won(void);

int main(int argc, string argv[])
{
    if (argc != 2)              // ensure proper usage
    {
        printf("Usage: fifteen d\n");
        return 1;
    }

    d = atoi(argv[1]);                  // ensure valid dimensions
    if (d < DIM_MIN || d > DIM_MAX)
    {
        printf("Board must be between %i x %i and %i x %i, inclusive.\n",
            DIM_MIN, DIM_MIN, DIM_MAX, DIM_MAX);
        return 2;
    }

    FILE *file = fopen("log.txt", "w");     // open log
    if (file == NULL)
        return 3;
        
    greet();        // greet user with instructions
    init();     // initialize the board
   
    while (true)            // accept moves until game is won
    {
        clear();             // clear the screen
        draw();     // draw the current state of the board

        for (int i = 0; i < d; i++)      // log the current state of the board (for testing)
        {
            for (int j = 0; j < d; j++)
            {
                fprintf(file, "%i", board[i][j]);
                if (j < d - 1)
                {
                    fprintf(file, "|");
                }
            }
            fprintf(file, "\n");
        }
        fflush(file);

        if (won())      // check for win
        {
            printf("ftw!\n");
            break;
        }

        printf("Tile to move: ");       // prompt for move
        int tile = get_int();
        
        if (tile == 0)      // quit if user inputs 0 (for testing)
            break;

        fprintf(file, "%i\n", tile);        // log move (for testing)
        fflush(file);

        if (!move(tile))        // move if possible, else report illegality
        {
            printf("\nIllegal move.\n");
            usleep(500000);
        }
        usleep(500000);     // sleep thread for animation's sake
    }

    fclose(file);       // close log
    return 0;       // success
}
/**
 * Clears screen using ANSI escape sequences.
 */
void clear(void)
{
    printf("\033[2J");
    printf("\033[%d;%dH", 0, 0);
}
/**
 * Greets player.
 */
void greet(void)
{
    clear();
    printf("WELCOME TO GAME OF FIFTEEN\n");
    usleep(2000000);
}
/**
 * Initializes the game's board with tiles numbered 1 through d*d - 1
 * (i.e., fills 2D array with values but does not actually print them).  
 */

void init(void)
{
    int total = d * d;      // Get Total number of spaces
    
    for (int i = 0; i < d; i++)     // Add tiles to board
    {
        for (int j = 0; j < d; j++)
        {
            board[i][j] = --total;          // Decrement value by one and assign to array
        }
    }
    if ((d * d) % 2 == 0)           // Swap 2 and 1 if even number of spaces
    {
        board[d - 1][d - 3] = 1;
        board[d - 1][d - 2] = 2;
    }
}
/**
 * Prints the board in its current state.
 */
void draw(void)
{
    for (int i = 0; i < d; i++)     // Loop through board array
    {
        for (int j = 0; j < d; j++)
        {
            if (board[i][j] == 0)       // Print line instead of zero
                printf("  _");
            else 
                printf("%3i", board[i][j]);
        }
        printf("\n\n");
    }
}
/**
 * If tile borders empty space, moves tile and returns true, else
 * returns false. 
 */
bool move(int tile)
{
    if (tile > d * d - 1 || tile < 1)       // Check if tile is valid
        return false;

    int row = 0, column = 0;        // Search board for column and row 
    
    for (int i = 0; i < d; i++)
    {
        for (int j = 0; j < d; j++)
        {
            if (board[i][j] == tile)
            {
                row = i;
                column = j;
            }
        }
    }

    if (row - 1 >= 0 && board[row - 1][column] == 0)        // Check the nearby spaces
    {
        board[row - 1][column] = board[row][column];
        board[row][column] = 0;
        return true;
    }
    else if (row + 1 < d && board[row + 1][column] == 0)
    {
        board[row + 1][column] = board[row][column];
        board[row][column] = 0;
        return true;
    }
    else if (column - 1 >= 0 && board[row][column - 1] == 0)
    {
        board[row][column - 1] = board[row][column];
        board[row][column] = 0;
        return true;
    }
    else if (column + 1 < d && board[row][column + 1] == 0)
    {
        board[row][column + 1] = board[row][column];
        board[row][column] = 0;
        return true;
    }
    return false;
}
/**
 * Returns true if game is won (i.e., board is in winning configuration), 
 * else false.
 */
bool won(void)
{
    int counter = 0;
    
    for (int i = 0; i < d; i++)     // Check each tile to ensure it's in order
    {
        for (int j = 0; j < d; j++)
        {
            if (++counter != (d * d) && board[i][j] != counter)     // Check if last spot and if not correct value
                return false;
        }
    }
    return true;
}