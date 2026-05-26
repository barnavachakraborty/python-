#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<time.h>
#include<math.h>
#include<ctype.h>


typedef unsigned char pix;

void unique_filename(char *output_filename, char ext[])
{
    FILE *fp;
    char name[200];
    size_t len = strcspn(output_filename,".");
    memcpy(name,output_filename,len);
    name[len] = '\0';
    char final[200];
    snprintf(final,sizeof(final),"%s%s",name,ext);
    int count = 0;

    while((fp = fopen(final,"r")))
    {
        fclose(fp);
        snprintf(final,sizeof(final),"%s(%d)%s",name,++count,ext);
    }

    snprintf(output_filename,200,"%s",final);
}

size_t* segmentation(pix *pixels,pix *pixels_out,int height,int width,int k)
{
    size_t pixels_count = (size_t)height*(size_t)width;
    long long int *sum = malloc(k*sizeof(long long ));
    size_t *count = malloc(k*sizeof(size_t)),*assignments = malloc(pixels_count*sizeof(size_t));
    float *centroids = malloc(k*sizeof(float)),*new_c = malloc(k*sizeof(float));
    if(!sum||!count||!assignments||!centroids||!new_c)
    {        printf("Couldn't allocate memory...");
        exit(0);
    }
    int i ;
    for(i = 0; i<k;i++) centroids[i] = rand()%256;
    
    int iter,max_iter = 100;
    for(iter = 0;iter<max_iter;iter++)
    {
        for (i = 0 ;i<pixels_count;i++)
        {
            int c;
            float best_distance = fabsf((float)pixels[i] - centroids[0]);
            int best = 0;
            for(c = 1;c<k;c++)
            {
                float d = fabsf((float)pixels[i] - centroids[c]);
                if(d<best_distance) 
                {
                    best_distance = d;
                    best = c;
                }
            }
            assignments[i] = best;
        }
        memset(sum,0,k*sizeof*sum);
        memset(count,0,k*sizeof*count);
        int c;
        for(c = 0 ; c< pixels_count;c++)
        {
            sum[assignments[c]] += pixels[c];
            count[assignments[c]]++;
        }
        int changed = 0;
        for(c = 0;c<k;c++)
        {
            if(count[c]>0) new_c[c] = (float)sum[c]/(float)count[c];
            else new_c[c] = rand() % 256;
            if(fabsf(centroids[c]-new_c[c])>=0.5f) changed = 1;
        }

        if(!changed) break;

        memcpy(centroids,new_c,k*sizeof(float));

    }
    for(i = 0;i<pixels_count;i++)
    {
        pixels_out[i] = (pix)round(centroids[assignments[i]]);
    }
    free(sum);
    free(count);
    free(centroids);
    free(new_c);
    return assignments;
}

typedef struct 
{
    pix r,g,b;
}segment;

int main()
{
    srand((unsigned)time(NULL));

    char input_file[200],output_file[200];

    printf("Enter your input file path: ");
    fgets(input_file,sizeof(input_file),stdin);
    input_file[strcspn(input_file,"\n")] = '\0';

    printf("Enter your output file path: ");
    fgets(output_file,sizeof(output_file),stdin);
    output_file[strcspn(output_file,"\n")] = '\0';

    if(input_file[0] == '"' && input_file[strlen(input_file)-1] == '"' )
    {
        size_t len = strlen(input_file);
        memmove(input_file,input_file+1,len-2);
        input_file[len-2] = '\0';
    }
    
    if(output_file[0] == '"' && output_file[strlen(output_file)-1] == '"' )
    {
        size_t len = strlen(output_file);
        memmove(output_file,output_file+1,len-2);
        output_file[len-2] = '\0';
    }
    
    char ext[] = ".ppm";
    unique_filename(output_file,ext);
    int k;
k_input:
    printf("Enter the number of sengments you want: ");
    scanf("%d",&k);
    if(k<=0)
    {
        printf("Inappropriate input for k...\n");
        goto k_input;
    }
    
    FILE *input = fopen(input_file,"r");
        if(!input)
        {
            printf("Couldnt open the file \"%s\"...",input_file);
            return 1;
        }
        char format[4] = {0};
        fscanf(input,"%2s",format);
        if (strcmp(format, "P2") != 0 && strcmp(format,"P3") != 0) 
        {
            fprintf(stderr, "Only ASCII PGM (P2) & ASCII PPM (P3) supported. Found: %s\n", format);
            fclose(input);
            return 1;
        }
        char c;
        while((c = fgetc(input)) != EOF)
        {
            if(isspace(c)) continue;
            if(c == '#')
            {
                while((c = fgetc(input)) != EOF && c != '\n') 
                    continue;
            }
            ungetc(c,input);
            break;
        }
        int height,width,maxval;
        fscanf(input,"%d %d %d",&width,&height,&maxval);
        pix *data[3],*data_out[3];
        FILE *output = fopen(output_file,"w");
        if(!output)
        {
            printf("Couldnt open the file \"%s\"...",output_file);
            return 1;
        }
        fprintf(output,"P3\n%d %d\n%d\n",width,height,maxval);
        if(strcmp(format,"P2") == 0)
        {
            data[0] = malloc((size_t)height*width*sizeof(pix));
            data_out[0] = malloc((size_t)height*width*sizeof(pix));
            for(int i = 0;i<height*width;i++)
            {
                int temp;
                fscanf(input,"%d",&temp);
                data[0][i] = (pix)temp;
            }
            size_t *segments = segmentation(data[0],data_out[0],height,width,k);
            
            segment *colours = malloc(k*sizeof(segment));
            colours[0].r = 255;
            colours[0].g = 0;
            colours[0].b = 0;
            colours[1].r = 0;
            colours[1].g = 255;
            colours[1].b = 0;
            colours[2].r = 0;
            colours[2].g = 0;
            colours[2].b = 255;
            colours[3].r = 0;
            colours[3].g = 0;
            colours[3].b = 0;
            colours[4].r = 255;
            colours[4].g = 255;
            colours[4].b = 255;
            for(int c = 5 ; c<k;c++)
            {
                colours[c].r = rand()%256;
                colours[c].g = rand()%256;
                colours[c].b = rand()%256;
            }
            for(int i = 0;i<height;i++)
            {
                for(int j = 0; j<width;j++)
                {
                    fprintf(output,"%d %d %d ",colours[segments[i*width+j]].r,colours[segments[i*width+j]].g,colours[segments[i*width+j]].b);
                }
                fputc('\n',output);
                
            }
            free(data[0]);
            free(data_out[0]);
            free(segments);
            free(colours);
        }
        else
        {
            for(int i = 0 ;i<3;i++)
            {
                data[i] = malloc((size_t)height*width*sizeof(pix));
                data_out[i] = malloc((size_t)height*width*sizeof(pix));
            }
            for(int i = 0;i<height*width;i++)
            {
                int temp[3];
                fscanf(input,"%d %d %d",&temp[0],&temp[1],&temp[2]);
                data[0][i] = (pix)temp[0];
                data[1][i] = (pix)temp[1];
                data[2][i] = (pix)temp[2];
            }
            segmentation(data[0],data_out[0],height,width,k);
            segmentation(data[1],data_out[1],height,width,k);
            segmentation(data[2],data_out[2],height,width,k);            
            
            for(int i = 0;i<height;i++)
            {
                for(int j = 0; j<width;j++)
                {
                    fprintf(output,"%d %d %d ",(int)data_out[0][i*width+j],(int)data_out[1][i*width+j],(int)data_out[2][i*width+j]);
                }
                fputc('\n',output);
            }
            for(int i = 0 ;i<3;i++)
            {
                free(data[i]);
                free(data_out[i]);
            }
        }
    fclose(output);
    fclose(input);
}