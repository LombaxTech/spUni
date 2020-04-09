#include<stdio.h>
#include<string.h>
#include <stdlib.h>
#include <stdbool.h>
#include<math.h>

////Global variables to hash the string input
//int V, U;
const MAXNODE = 8;


// enum type to state the form of the input circuit element 
//N is initial state, R is series resistance, G is shunt resistance and M is in ACBD matrix form. 
typedef enum { r, g, M, N } type;
//enum type to state the form of the connection
typedef enum {shunt, series, No} Connection;



//count the elements imported to the program. 
int counting = 0, Scounting = 0, Rcounting = 0;

// final output matrix 
float An = 1, Bn = 0, Cn = 0, Dn = 1;
//intermediate output matrix
float Ai = 0, Bi = 0, Ci = 0, Di = 0;

//predefine array to hold the right order of the matrix multiplication
int array_n1[50] = { 0,1, 2,1, 0,2, 3,2, 0,3, 4,3, 0,4, 5,4, 0,5, 6,5 ,6,0,7,6,7,0, 7,8, 0,8, 8,9,9,0};
int array_n2[50] = { 1,0, 1,2, 2,0, 2,3, 3,0, 3,4, 4,0, 4,5, 5,0, 5,6, 0,6,6,7, 0,7, 8,7, 8,0,9,8,0,9};
//array that holds the output quantities
float array_output[20];
//array that holds the order of the output
int array_Final[20];
//array that holds the dB flag for each variable. 
int array_dB[20];


FILE *fp, *fs, *ft;//fp is the pointer to the source data file, fs is the pointer to the output file.ft is the file to be compared with the input file

//Linked list to arrange the circuit elements 
struct node {
	int n1, n2;
	float R;
	float G;
	float A, B, C, D;

	enum type Type;
	enum connection SubConnection;

	struct node *next;
	struct node *prev;
};
//linked list to hold the output variable names, units and values
struct output {
	char variable[30];
	char unit[30];
	float outputValue;

	struct output *next;
	struct output *prev;
};

//Position indicator used in <cicuit> Block
struct node *head = NULL;
struct node *last = NULL;
struct node *current = NULL;

//Postion indicator used in <output> Block
struct output *ohead = NULL;
struct output *olast = NULL;
struct output *ocurrent = NULL;


/*prototype declaration*/
//function to find the integer after string ident
int find_int(char *buffer, char *ident, int ok);
//function to find the integer after string ident
float find_float(char *buffer[100], char *ident[100], int ok);
//function to insert item to the linked list
void insertFirst(int n1, int n2, float R, float G, type Type);
//function to insert item to the linked list
void insertLast(char variable[], char unit[]);
//display the linked list
void displayForward();
int OdisplayForward(int array[]);
//calculate the output values and store them in a fixed array.
float calculateValue(float array[],float An, float Bn, float Cn, float  Dn, float VT, float  ZS, float ZL);


//check whether the linked list is empty
bool isEmpty();
bool OisEmpty();

//set the unit according to the input
char unitSetting(char variable[], char unit);

//change the dB to dBV/dBI/dBW/dB according to the variable type.
char dBSetting(char variable[], char unit[]);
void dBTransfer(float array_output[], int array_Final[], int array_dB[],int m);


//function used to calculate and delete 1 link from the list. 
struct node* delete(int n1, int n2);



/*start of the main function*/
int main()
{
	/*variable declaration*/

	//temperary counting for "for" loop.
	int i = 0, p = 0;

	char buffer[100];// this buffer is used to shortly store content in a whole line in the source file
	char filename[100]="0";// this string is used to store name specified in source file
	char variable[30], unit[30];// used to buffer variable and unit specified in output block

	//replica of node numbers of the circuit element being analysed. 
	int n1 = 0, n2 = 0;

	//temporary value for R and G value from the input data file waiting to be stored in the linked list.
	float R = 0, G = 0;
	float A = 0, B = 0, C = 0, D = 0;

    // output node which represent the end of the cascaded circuit. 
	int nF;

	// input voltage, source resistor and load resistor. 
	float VT = -1, RS = -1, RL = -1, GS = -1, IN = -1;

	//NEEDLES for find_float, find_string and so on
	char needle[100];

	//FLAG set if item is found
	int FLAG = 0;

	//flags show the poosition of the reading cursor which determines the state of the program
	enum flag { circuit, term, output, stay } flag = stay;
	
	type MainType = N;
	Connection MainConnection = No;
	//printf("%d", MainType);

	//initialize the arrays
	while (i < 20)
	{
		array_dB[i] = 0;
		array_Final[i] = -1;
		i++;
	}
	//initialize i
	i = 0;

	/*main program*/

	 fopen_s(&fp,"ABCD_input.dat", "rt");// open the specific data file in read in text mode. 
	// TESTING: code below checks the validity of file pointer. 
	if (fp == NULL)
	{
		perror("Error :  ");
		return(-1);
	}
	printf("ABCD_input.txt opened for reading OK\n");// indication of source file is opened. 

	//test file used to be compared with the input file
	fopen_s(&ft, "test.dat", "wt");

	//find the output block and create the file with the name specified in it.
	//set the term variables ahead of the circuit element input to test 
	while (fgets(buffer, sizeof buffer, fp))
	{
		fprintf(ft, "%s", buffer);
		//ignore the text
		if (*buffer == '#')
		{
			continue;
		}
		
		//open the file specified
		if (sscanf_s(buffer, "File_name=%s", filename, _countof(filename)) == 1)
		{
			fs = fopen(filename, "w");
			printf("file opened for writing OK");
		}
		/*else
		{
			
		}*/

	   if (strcmp(buffer, "<TERMS>\n") == 0)// if <TERMS> comes, change state of the block to "TERMS". 
	   {
		    flag = term;
		/*    printf("\nTERM!!\n");*/

	   }
	   else if ( strcmp (buffer, "</TERMS>\n") == 0)  //if </TERMS> comes, change state of the block back to "stay".
	   {
		     flag = stay;
	   }
	   if ( flag == term ) 
	   {
		   //find values for each variable
		   strcpy(needle, "VT");
		   if (VT < 0)
		   {
			   VT = find_float(buffer, needle, FLAG);
		   }
		   strcpy(needle, "IN");
		   if(IN <0) 
		   {
			   IN = find_float(buffer, needle, FLAG);
		   }
		   
		   strcpy(needle, "RS");
		   if (RS < 0)
		   {
			   RS = find_float(buffer, needle, FLAG);
		   }
		  
		   strcpy(needle, "GS");
		   if (GS < 0)
		   {
			   GS = find_float(buffer, needle, FLAG);
		   }
		   

		   if (GS != -1)
		   {
			   RS = 1 / GS;
			   printf("\n[RS transfered from GS%f]\n", RS);
		   }
		   if (IN != -1)
		   {
			   VT = IN * RS;
		   }
		   //{
			  // /*fprintf(fs, "**VT = %d, RS =%d  \n", VT, RS);*/
			  ///* printf("**VT = %d, RS =%d  \n", VT, RS);*/
		   //}
		   if (sscanf_s(buffer, "%d RL=%f\n", &nF, &RL) == 2)
		   {
			   if (((nF!=-1)&&(nF < 0))||(nF > MAXNODE))
			   {
				   printf("\nload node value exceed the range !\n");
				   exit(-1);
			   }
		   }
		   //{
			  // /*fprintf(fs, "**final Node = %d, RL =%d  \n", VT, RS);*/
			  ///* printf("**final Node = %d, RL =%d  \n", VT, RS);*/
		   //}
	   };
	}

	//print the <TERMS>
	printf("\n[%d][%f][%f][%f][%f]\n", nF, IN, RL, RS, VT);

	//if the output file name is not defined in the input data file... 
	if (fs == NULL)
	{
		printf("\noutput file name is not defined !!!!\n");
		exit(-1);
	}


	rewind(fp);// after reading the whole file, restart the position of the cursor.

	//main reading block
	while (fgets(buffer, sizeof buffer, fp))// read a new line when it is not the end of the file(EOF)
	{
		/*________________________________________________________________________________*/
		if (*buffer == '#')
		{
			continue;
		}
		/*________________________________________________________________________________*/

		//printf("%s\n", buffer);// pirnt what the fgets() function reads into the buffer
		Rcounting++;
		if (strcmp(buffer, "<CIRCUIT>\n") == 0)// if <CIRCUIT> comes, change state of the block to "circuit"
		{
			flag = circuit;
			/*printf("\nCIRCUIT!!\n");*/
		}
		else if (strcmp(buffer, "</CIRCUIT>\n") == 0)// if </CIRCUIT> comes, change state of the block back to "stay".
		{
			flag = stay;
		}

		

		else if (strcmp(buffer, "<OUTPUT>\n") == 0)// if <OUTPUT> comes, change state of the block to "output".
		{
			flag = output;
		}
		else if (strcmp(buffer, "</OUTPUT>\n") == 0)// if </OUTPUT> comes, change state of the block back to "stay".
		{
			flag = stay;
		}
		else
			printf("");// if the line which the cursor is in does not have state changing content, do nothing. 

		//the structural block that distribute the data according to the state of the program set by the flags. 
		switch (flag)// change the state of the block according to the 
		{
		
		//the case circuit will be the main block of the calculation part. 
		case (circuit):
		{
			//find nodes
			strcpy(needle, "n1");
			printf("", n1 = find_int(buffer, needle, FLAG));
			
			strcpy(needle, "n2");
			printf("", n2 = find_int(buffer, needle, FLAG));
			//sanity check
			if ((abs(n1 - n2) > 1) && (n1*n2 != 0))
			{
				printf("\nERROR:n1 and n2 are not adjacent !\n");
				exit(-1);
			}
			if ((n1 > nF) || (n2 > nF))
			{
				printf("\nERROR:node is not in range\n");
				exit(-1);
			}
			// Check the shunt& series connection of the circuit element. 
			if (n1*n2 == 0)
			{
				MainConnection = shunt;
			}
			else if ((n1 != 0) && (n2 != 0))
			{
				MainConnection = series;
			}
			/*printf("\n[MainConnection%d]\n", MainConnection);*/
			/*R input*/
			strcpy(needle, "R");
			printf("",  R = find_float(buffer, needle, FLAG));
			if (R >= 0 )
			{
				MainType = r;

				counting++;
			}
	/*		printf("%d", MainType);*/
			/*R input*/

			/*G input*/
			strcpy(needle, "G");
			printf("", G = find_float(buffer, needle, FLAG));
			if (G >=0)
			{
				if (counting > 0)
				{
					printf("\nmultiple input of R and G in row (%d)\n", Rcounting);
					return -1;
				}
				MainType = g; 
				counting++; 
			}
			//printf("%d", MainType);
			/*G input*/

			/*ABCD input*/
			strcpy(needle, "A");
			printf("", A = find_float(buffer, needle, FLAG));
			if (A >= 0 )
			{
				if (counting > 0)
				{
					printf("multiple input of R and G or ABCDin row (%d)", Rcounting);
					return -1;
				}
				
				Scounting++;
			}

			strcpy(needle, "B");
			printf("", B = find_float(buffer, needle, FLAG));
			if (B >= 0)
			{
				if (counting > 0)
				{
					printf("multiple input of R and G or ABCDin row (%d)", Rcounting);
					return -1;
				}
		
				Scounting++;
			}

			strcpy(needle, "C");
			printf("", C = find_float(buffer, needle, FLAG));
			if (C >= 0)
			{
				if (counting > 0)
				{
					printf("multiple input of R and G or ABCDin row (%d)", Rcounting);
					return -1;
				}
			
				Scounting++;
			}

			strcpy(needle, "D");
			printf("", D = find_float(buffer, needle, FLAG));
			if (D >= 0 )
			{
				if (counting > 0)
				{
					printf("multiple input of R and G or ABCDin row (%d)", Rcounting);
					return -1;
				}

				Scounting++;
				if (Scounting == 4)
				{
					MainType = M;

				}
				else
				{
					printf("there is a invalid input in ABCD ");
					return -1; 
				}
				Scounting = 0;
			}
	/*		printf("%d", MainType);*/
			counting = 0; 
			/*ABCD input*/

			if (  ((n1 != -1) && (n2 != -1))  &&  (MainType != N)  )
			{
				/*printf("\n[MainType%d]\n", MainType);*/
				insertFirst(n1, n2, R, G, MainType, MainConnection);
			}
		};
		break;
	
		case(output):
		{

			if (sscanf_s(buffer, "%s %s\n", variable, _countof(variable), unit,_countof(unit) ) == 2)
			{
				if (strlen(variable) > 4)
				{

				}
				else
				{
					dBSetting(variable, unit);
					/*fprintf(fs, "variable : %s unit : %s \n", variable, unit);*/
					/*printf("variavle : %s   unit : %s \n", variable, unit);*/
					insertLast(variable, unit);

				}
			}
			if (sscanf_s(buffer, "%s %s\n", variable, _countof(variable), unit, _countof(variable) ) == 1)
			{
				if (strlen(variable) > 4)
				{
				}
				else
				{
					/*fprintf(fs, "variable : %s  \n", variable, unit);*/
					/*printf("variavle : %s  \n", variable, unit);*/
					unitSetting(variable, unit);
					/*strcpy(unit, "unit");*/

					//计数， 动态分配矩阵大小
					insertLast(variable, unit);

				}
			}

		};
		break;

		default:
			break;
		}
	}

	//print the arrays
	displayForward();
	OdisplayForward(array_Final);

	//calculate the matrix from the linked list and delete...
	//outer while loop navigate all the possible nodes in sequence. 
	//inner while loop navigate the linked list to check whether.
	//the specified n1 n2 exist in the list.
	while (i < 30)
	{
		p = 0;
		while ((delete(array_n1[i], array_n2[i])) != NULL) { p++; };
	// nodes missing error? 
		i++;
	}

	//calcualte the variable values
	printf("\n[%f  %f\n %f %f]\n", An, Bn, Cn, Dn);
	calculateValue(array_output, An, Bn, Cn, Dn, VT, RS, RL);


	fprintf(fs, "\n");
	i = 0;

	//Arrangement of the output numbers... 
	//As the linked list is deleted after calculating,
	//the reading from the output and term blocks can only be stored in an array.
	while (i < 20)
	{
		
		if (array_Final[i] == -1)
		{
			break;
		}
		dBTransfer(array_output, array_Final, array_dB, i);
		if (array_output[(int)(array_Final[i])] < 0)
		{
			fprintf(fs, " %.4e", array_output[(int)(array_Final[i])]);
		}
		else fprintf(fs, "  %.4e", array_output[(int)(array_Final[i])]);
		if (array_Final[i + 1] != -1)
		{
			fprintf(fs, ", ");
		}
	

		printf("  %.4e, [%d]", array_output[(int)(array_Final[i])], array_Final[i]);
		/*printf("\n[  %.4e, ]\n", array_output[i]);*/
		i++;
	}

	fprintf(fs, "\n\n");// to meet the file format
	
	
	fclose(fp);
	fclose(fs);

	//the main function returns 0 when it is successfully operated. 
	return 0;

}
/* end of main function */



/*
Subfunction used to find float value
*/
int find_int(char *buffer[100], char *ident[100], int ok)
{
	char *pch, *pch2;
	int rtn = -1;//(float)(-1.234567);
	int ifound, value_found = 0, ident_found = 0, equals_found = 0, i_ok = 0;

	//firstly find the first occurrence of the desired sub-string. 
	pch = strstr(buffer, ident);

	//if the string is found, go on. 
	if (pch != NULL)
	{
		ident_found = 1;
		pch2 = strchr(pch, '=');
		
		//continue if the '='(i.e. the equal sign) is found. 
		if (pch2 != NULL)
		{
			equals_found = 1;
			ifound = sscanf_s((pch2 + 1), "%d", &rtn);
			//printf("\n%f\n", rtn);
			value_found = (int)(ifound == 1);
			if (value_found == 0)
			{
				printf("\nInterger value is not valid! \n");
				exit(-1);
			}
			if ( (rtn != -1) && (rtn < 0))
			{
				printf("\n node is not in range \n");
				exit(-1);
			}
			i_ok = 1;
		}
		else
		{
			i_ok = -1;
		}
	}
	else
	{
		i_ok = -2;
	}
	ok = &i_ok;
	/*printf("%d\n", i_ok);*/

	return(rtn);
}

float find_float(char *buffer[100], char *ident[100], int ok)
{
	char *pch, *pch2;
	float rtn = -1.000000;//(float)(-1.234567);
	int ifound, value_found = 0, ident_found = 0, equals_found = 0, i_ok = 0;

	//firstly find the first occurrence of the desired sub-string. 
	pch = strstr(buffer, ident);

	//if the string is found, go on. 
	if (pch != NULL)
	{
		ident_found = 1;
		pch2 = strchr(pch, '=');

		//continue if the '='(i.e. the equal sign) is found. 
		if (pch2 != NULL)
		{
			equals_found = 1;
			ifound = sscanf_s((pch2 + 1), "%f", &rtn);
	
			//printf("\n%f\n", rtn);
			value_found = (int)(ifound == 1);
			if (value_found != 1)
			{
				printf("\nFloat value is not valid!!!\n");
				exit(-1);
			}
			i_ok = 1;
		}
		else
		{
			i_ok = -1;
		/*	printf("= is not found !!!");
			exit(-1);*/
		}
	}
	else
	{
		i_ok = -2;
	}
	ok = i_ok;
	/*printf("%d\n", i_ok);*/
	//printf("\n%f\n", rtn);
	return(rtn);
}

void insertFirst(int n1, int n2, float R, float G, type Type, Connection SubConnection) {

	//create a link
	struct node *link = (struct node*) malloc(sizeof(struct node));
	link->n1 = n1;
	link->n2 = n2;
	link->R = R;
	link->G = G;
	link->Type = Type;
	link->SubConnection = SubConnection;

	if (isEmpty()) {
		//make it the last link
		last = link;
	}
	else {
		//update first prev link
		head->prev = link;
	}

	//point it to old first link
	link->next = head;

	//point first to new first link
	head = link;
}

void insertLast(char variable[], char unit[]) {

	//create a link
	struct output *olink = (struct output*) malloc(sizeof(struct output));

	strcpy(olink->variable, variable);
	strcpy(olink->unit, unit);

	if (OisEmpty()) {
		//make it the last link
		ohead = olink;
	}
	else {
		//make link a new last link
		olast->next = olink;
	}
	//mark old last node as prev of new link
	olink->prev = olast;


	//point last to new last node
	olast = olink;

}



void displayForward() {

	//start from the beginning
	struct node *ptr = head;

	//navigate till the end of the list
	printf("\n[ ");

	while (ptr != NULL) {
		printf("(%d,%d) ", ptr->n1, ptr->n2);
		ptr = ptr->next;
	}

	printf(" ]");
}

int OdisplayForward(int array[]) {

	//start from the beginning
	struct output *ptr = olast;

	int k = 0;
	/*printf("\n[ ");*/
	printf("\n");

	//navigate till the end of the list
	while (ptr->prev != NULL) {
		/*	printf("(%s,%s) ", ptr->variable, ptr->unit);*/
		ptr = ptr->prev;
	}

	//Navigate in the opposite direction with above navigation
	//ARRANGE the output volumes. 
	while (ptr != olast) {
		printf("%s, ", ptr->variable);

		fprintf(fs, "%s, ", ptr->variable);

		if (strcmp(ptr->variable, "Vin") == 0)
		{
			array_Final[k] = 6;
		}
		else if (strcmp(ptr->variable, "Vout") == 0)
		{
			array_Final[k] = 7;
		}
		else if (strcmp(ptr->variable, "Iin") == 0)
		{
			array_Final[k] = 8;
		}
		else if (strcmp(ptr->variable, "Iout") == 0)
		{
			array_Final[k] = 9;
		}
		else if (strcmp(ptr->variable, "Pin") == 0)
		{
			array_Final[k] = 10;
		}
		else if (strcmp(ptr->variable, "Zout") == 0)
		{
			array_Final[k] = 1;
		}
		else if (strcmp(ptr->variable, "Pout") == 0)
		{
			array_Final[k] = 11;
		}
		else if (strcmp(ptr->variable, "Zin") == 0)
		{
			array_Final[k] = 0;
		}
		else if (strcmp(ptr->variable, "Av") == 0)
		{
			array_Final[k] = 2;
		}
		else if (strcmp(ptr->variable, "Ai") == 0)
		{
			array_Final[k] = 3;
		}
		else if (strcmp(ptr->variable, "Ap") == 0)
		{
			array_Final[k] = 4;
		}

		ptr = ptr->next;
		k++;
	}


	//as the list is built from last to the head, we can not get to the last when navigating.
	//this line compensate for this .
	printf("%s", olast->variable);

	fprintf(fs, "%s", olast->variable);
	if (strcmp(ptr->variable, "Vin") == 0)
	{
		array_Final[k] = 6;
	}
	else if (strcmp(ptr->variable, "Vout") == 0)
	{
		array_Final[k] = 7;
	}
	else if (strcmp(ptr->variable, "Iin") == 0)
	{
		array_Final[k] = 8;
	}
	else if (strcmp(ptr->variable, "Iout") == 0)
	{
		array_Final[k] = 9;
	}
	else if (strcmp(ptr->variable, "Pin") == 0)
	{
		array_Final[k] = 10;
	}
	else if (strcmp(ptr->variable, "Zout") == 0)
	{
		array_Final[k] = 1;
	}
	else if (strcmp(ptr->variable, "Pout") == 0)
	{
		array_Final[k] = 11;
	}
	else if (strcmp(ptr->variable, "Zin") == 0)
	{
		array_Final[k] = 0;
	}
	else if (strcmp(ptr->variable, "Av") == 0)
	{
		array_Final[k] = 2;
	}
	else if (strcmp(ptr->variable, "Ai") == 0)
	{
		array_Final[k] = 3;
	}
	else if (strcmp(ptr->variable, "Ap") == 0)
	{
		array_Final[k] = 4;
	}

	printf("\n");
	fprintf(fs, "\n");


	k = 0;
	while (ptr->prev!= NULL) {
		/*	printf("(%s,%s) ", ptr->variable, ptr->unit);*/
		ptr = ptr->prev;
	}
	while (ptr != olast) {
		printf("%s, ", ptr->unit);

		fprintf(fs, "%s, ", ptr->unit);
		/*printf("\n[unit%s]\n", ptr->unit);*/
		if ((strcmp(ptr->unit,"dBV")==0)|| (strcmp(ptr->unit, "dBW")==0)|| (strcmp(ptr->unit, "dB")==0)|| (strcmp(ptr->unit, "dBI")==0))
		{
			array_dB[k] = 1;
		}
		else array_dB[k] = 0;
		/*printf("\n[array_dB%d]\n", array_dB[k]);*/
		k++;
		
		ptr = ptr->next;
	}

	/*printf("%s", olast->unit);*/
	/*printf("\n[unit%s]\n", ptr->unit);*/
	fprintf(fs, "%s", olast->unit);
	if ((strcmp(ptr->unit, "dBV") == 0) || (strcmp(ptr->unit, "dBW") == 0) || (strcmp(ptr->unit, "dB") == 0) || (strcmp(ptr->unit, "dBI") == 0))
	{
		array_dB[k] = 1;
	}
	else array_dB[k] = 0;
	printf("\n[array_dB%d]\n", array_dB[k]);


	/*printf(" ]");*/
}




bool isEmpty() {
	return head == NULL;
}
bool OisEmpty() {
	return ohead == NULL;
}

char unitSetting(char variable[], char unit[]) 
{
	if (strcmp(variable, "Vin") == 0)
	{
		strcpy(unit, "V");
	}
	else if (strcmp(variable, "Vout") == 0)
	{
		strcpy(unit, "V");
	}
	else if (strcmp(variable, "Iin") == 0)
	{
		strcpy(unit, "I");
	}
	else if (strcmp(variable, "Iout") == 0)
	{
		strcpy(unit, "I");
	}
	else if (strcmp(variable, "Pin") == 0)
	{
		strcpy(unit, "W");
	}
	else if (strcmp(variable, "Zout") == 0)
	{
		strcpy(unit, "Ohm");
	}
	else if (strcmp(variable, "Pout") == 0)
	{
		strcpy(unit, "W");
	}
	else if (strcmp(variable, "Zin") == 0)
	{
		strcpy(unit, "Ohm");
	}
	else if (strcmp(variable, "Av") == 0)
	{
		strcpy(unit, "L");
	}
	else if (strcmp(variable, "Ai") == 0)
	{
		strcpy(unit, "L");
	}
	else if (strcmp(variable, "Ap") == 0)
	{
		strcpy(unit, "L");
	}

}

char dBSetting(char variable[], char unit[])
{
	if ((strcmp(variable, "Vin") == 0)&&(strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBV");
	}
	else if ((strcmp(variable, "Vout") == 0) && (strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBV");
	}
	else if ((strcmp(variable, "Iin") == 0) && (strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBI");
	}
	else if ((strcmp(variable, "Iout") == 0) && (strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBI");
	}
	else if ((strcmp(variable, "Pout") == 0) && (strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBW");
	}
	else if ((strcmp(variable, "Pin") == 0) && (strcmp(unit, "dB") == 0))
	{
		strcpy(unit, "dBW");
	}
	
}

struct node* delete(int n1, int n2) {

	//start from the first link
	struct node* current = head;
	struct node* previous = NULL;

	//if list is empty
	if (head == NULL) {
		return NULL;
	}

	//navigate through list
	while (!(  ((current->n1) == n1)   &&  ((current->n2) == n2 )   )) {
		//if it is last node
		if (current->next == NULL) {
			return NULL;
		}
		else {
			//store reference to current link
			previous = current;

			//move to next link
			current = current->next;
		}
	}

	/*calculation part*/
	/*printf("\ncurrent->type[%d]\n",current->Type );*/
	if ((current->SubConnection == shunt)&&(current->Type == r))
	{
		current->G = 1.000000 / current->R;
	}
	else if ((current->SubConnection == series) && (current->Type == g))
	{
		current->R = 1.000000 / current->G; 
	}
	switch (current->SubConnection)
	{
	    case series:
		    current->A = 1; 
		    current->B = current->R;
		    current->C = 0;
		    current->D = 1;
		    break;
		case shunt:
			current->A = 1;
			current->B = 0;
			current->C = current->G;
			current->D = 1;
			break;
		case M:
			break;
	default:
		
		break;
	}
	/*printf("\n[%f   %f]\n", current->R, current->G);
	printf("\n[%f  %f  %f  %f] \n", current->A, current->B, current->C, current->D);
	printf("\n***[%f  %f\n %f %f]", An, Bn, Cn, Dn);
	printf("\n***[%f  %f\n %f %f]", Ai, Bi, Ci, Di);*/
	//multiply the intermediate matrix with the matrix conversed above.
	Ai = An * current->A + Bn * current->C;
	Bi = An * current->B + Bn * current->D;
	Ci = Cn * current->A + Dn * current->C; 
	Di = Cn * current->B + Dn * current->D;
    
	//transfer the intermediate matrix to the output matrix. 
	An = Ai, Bn = Bi, Cn = Ci, Dn = Di;
	/*printf("\n[%f  %f\n %f %f]", An, Bn, Cn, Dn);*/



	//found a match, update the link
	if (current == head) {
		//change first to point to next link
		head = head->next;
	}
	else {
		//bypass the current link
		current->prev->next = current->next;
	}

	if (current == last) {
		//change last to point to prev link
		last = current->prev;
	}
	else {
		current->next->prev = current->prev;
	}

	return current;
}

float calculateValue(float array[], float An, float Bn, float Cn, float Dn, float VT, float ZS, float ZL)
{
	float Zin, Zout, Av, Ai, Ap, T, YL, V1, Vout, Iin, Iout, Pin, Pout;
	int j;
	Zin = (An*ZL + Bn) / (Cn*ZL + Dn);//
	Zout = (Dn*ZS + Bn) / (Cn*ZS + An);//
	YL = 1 / ZL;//
	Av = 1 / (An + Bn * YL);//
	Ai = 1 / (Cn*ZL + Dn);//
	Ap = Av * Ai;
	T = 2 / (An*ZL + Bn + Cn * ZL*ZS + Dn * ZS);
	V1 = Zin * VT / (ZS + Zin);//
	Vout = V1 * Av; //
	Iin = VT / (ZS + Zin);//
	Iout = Ai * Iin;
	Pin = V1 * Iin;
	Pout = Pin * Ap;




	array[0] = Zin;
	array[1] = Zout;
	array[2] = Av;
	array[3] = Ai;
	array[4] = Ap;
	array[5] = T;
	array[6] = V1;
	array[7] = Vout;
	array[8] = Iin;
	array[9] = Iout;
	array[10] = Pin;
	array[11] = Pout;

	//for (j = 0; j < 9; j++)
	//{
	
	//}


}


void dBTransfer(float array_output[], int array_Final[], int array_dB[], int m )
{
    if ((array_dB[m]==1)&&(array_Final[m] != 10)&&(array_Final[m] != 11))
    {
	array_output[(int)(array_Final[m])] = 20 * log10(array_output[(int)(array_Final[m])]);
	}
	if ((array_dB[m] == 1) && ((array_Final[m] == 10) || (array_Final[m] == 11)))
	{
		array_output[(int)(array_Final[m])] = 10 * log10(array_output[(int)(array_Final[m])]);
	}
}