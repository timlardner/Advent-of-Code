    #include <stdio.h>
    #include <stdlib.h>
    #include <sys/time.h>

    char* ReadFile(char *filename)
    {
        char *buffer = NULL;
        size_t string_size, read_size;
        FILE *handler = fopen(filename, "r");
        if (handler)
        {
            fseek(handler, 0, SEEK_END);
            string_size = (size_t)ftell(handler);
            rewind(handler);
            buffer = (char*) malloc(sizeof(char) * (string_size + 1) );
            read_size = fread(buffer, sizeof(char), string_size, handler);
            buffer[string_size] = '\0';
            if (string_size != read_size)
            {
                free(buffer);
                buffer = NULL;
            }
            fclose(handler);
        }
        return buffer;
    }

    int main(int argc, char** argv)
    {
        char* filename;
        if (argc>1){
            filename = argv[1];
        } else {
            filename = "/Users/tim/Development/AoC/Day 13/input2.txt";
        }
        char *string = ReadFile(filename);
        struct timeval stop, start;
        int i = 0;
        int n_lines = 0;
        while (string[i] != '\0'){
            if (string[i] == ':'){
                n_lines++;
            }
            i++;
        }
        short *positions = malloc(n_lines * sizeof(short));
        short *depth = malloc(n_lines * sizeof(short));
        char *end = string;
        short pos = 0;
        short pospos = 0;
        while(*end) {
            long n = strtol(string, &end, 10);
            if (pos==0){
                positions[pospos] = n;
                pos = 1;
            } else {
                depth[pospos] = (n-1)*2;
                pos = 0;
                pospos++;
            }
            while (*end == ':' || *end == '\n') {
                end++;
            }
            string = end;
        }
        float time;
        int offset;
        short caught_yet;
        short idx;

        gettimeofday(&start, NULL);
        offset = 0;
        while (1) {
            caught_yet = 0;
            for (idx = 0; idx < n_lines; idx++) {
                if ((positions[idx] + offset) % depth[idx] == 0) {
                    caught_yet = 1;
                    break;
                }
            }
            if (caught_yet == 0) {
                break;
            }
            offset++;
        }
        gettimeofday(&stop, NULL);
        time = (stop.tv_sec * 1e6 + stop.tv_usec) - (start.tv_sec * 1e6 + start.tv_usec);
        printf("Best offset is %d\n", offset);
        printf("Took %f ms\n", (time) / 1e3);
        return 0;

    }