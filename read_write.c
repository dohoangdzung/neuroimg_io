#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <string.h>

int main(int argc, char ** argv)
{

    if(argc != 4)
    {
        printf("usage: read_write <file_in> <file_out> <log_file>\n");
        return 1;
    }

    // Parse arguments
    char * in_file_name = argv[1];
    char * out_file_name = argv[2];
    char * log_file_name = argv[3];


    FILE * log_file = fopen(log_file_name, "a");

    struct timeval  start;
    struct timeval  end;

    printf("\n----------------BEFORE READ-%s-----------------\n", in_file_name);
    printf("\nFile %s \n", in_file_name);
    char fincore[200];
    strcpy(fincore, "fincore -justsummarize ");
    strcat(fincore, in_file_name);
    system(fincore);
    printf("\nFile file2.dat\n");
    system("fincore -justsummarize output/file2.dat");
    printf("\nFile file3.dat\n");
    system("fincore -justsummarize output/file3.dat");
    printf("\nFile file4.dat\n");
    system("fincore -justsummarize output/file4.dat");

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

    double start_in_mill = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    double end_in_mill = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    fprintf(log_file, "read_start: %lf\n", start_in_mill);
    fprintf(log_file, "read_end: %lf\n", end_in_mill);
    printf("Read in: %lf", (end_in_mill - start_in_mill) / 1000);

    printf("\n----------------AFTER READ-%s-----------------", in_file_name);
    printf("\nFile %s \n", in_file_name);
    strcpy(fincore, "fincore -justsummarize ");
    strcat(fincore, in_file_name);
    system(fincore);
    printf("\nFile file2.dat\n");
    system("fincore -justsummarize output/file2.dat");
    printf("\nFile file3.dat\n");
    system("fincore -justsummarize output/file3.dat");
    printf("\nFile file4.dat\n");
    system("fincore -justsummarize output/file4.dat");

    // Increment buffer
    long int i;
    for(i = 0 ; i < fsize ; i++)
        buff[i]++;

    printf("\n----------------BEFORE WRITE-%s-----------------", out_file_name);
    printf("\nFile %s \n", in_file_name);
    strcpy(fincore, "fincore -justsummarize ");
    strcat(fincore, in_file_name);
    system(fincore);
    printf("\nFile file2.dat\n");
    system("fincore -justsummarize output/file2.dat");
    printf("\nFile file3.dat\n");
    system("fincore -justsummarize output/file3.dat");
    printf("\nFile file4.dat\n");
    system("fincore -justsummarize output/file4.dat");

    gettimeofday(&start, NULL);
//     Write buffer
//    FILE * out_file = fopen(out_file_name, "wb");
//    fwrite(buff, fsize, 1, out_file);
//    fclose(out_file);
    gettimeofday(&end, NULL);

    start_in_mill = (start.tv_sec) * 1000 + (start.tv_usec) / 1000 ;
    end_in_mill = (end.tv_sec) * 1000 + (end.tv_usec) / 1000 ;

    fprintf(log_file, "write_start: %lf\n", start_in_mill);
    fprintf(log_file, "write_end: %lf\n", end_in_mill);
    printf("Write in: %lf", (end_in_mill - start_in_mill) / 1000);

    printf("\n----------------AFTER WRITE-%s-----------------", out_file_name);
    printf("\nFile %s \n", in_file_name);
    strcpy(fincore, "fincore -justsummarize ");
    strcat(fincore, in_file_name);
    system(fincore);
    printf("\nFile file2.dat\n");
    system("fincore -justsummarize output/file2.dat");
    printf("\nFile file3.dat\n");
    system("fincore -justsummarize output/file3.dat");
    printf("\nFile file4.dat\n");
    system("fincore -justsummarize output/file4.dat");

    printf("===================================================================\n");

    fclose(log_file);

    return 0;
}