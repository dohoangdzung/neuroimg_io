#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

int main(int argc, char ** argv)
{

    if(argc != 3)
    {
        printf("usage: read_write <file_in> <log_file>\n");
        return 1;
    }

    // Parse arguments
    char * in_file_name = argv[1];
    char * log_file_name = argv[2];


    FILE * log_file = fopen(log_file_name, "a");

    struct timeval  start;
    struct timeval  end;

    printf("\nFile %s \n", in_file_name);
    gettimeofday(&start, NULL);
    // Get file size
    FILE * in_file = fopen(in_file_name, "rb");
    fseek(in_file, 0, SEEK_END);
    long fsize = ftell(in_file);
    fseek(in_file, 0, SEEK_SET);  

    // Read file in buffer
    char * buff = malloc(fsize + 1);
    fread(buff, fsize, 1, in_file);
    fclose(in_file);
    gettimeofday(&end, NULL);

    // Increment buffer
    long int i;
    for(i = 0 ; i < fsize ; i++)
        buff[i]++;

    double start_in_mill = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    double end_in_mill = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    fprintf(log_file, "read_start: %lf\n", start_in_mill);
    fprintf(log_file, "read_end: %lf\n", end_in_mill);
    printf("Read in: %lf\n", (end_in_mill - start_in_mill) / 1000);
    printf("Avg bw: %4.2lf MBps\n", fsize / ((end_in_mill - start_in_mill) * 1024));

    fclose(log_file);

    return 0;
}