#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct product {
	char *name;
	float* price;
	float* profit;
};

void muistinnollaus(struct product *array, int size)
{
    for (int i = 0; i < size; i++) { //Nollataan arrayn jokaiselle elementille varatut muistit
        free(array[i].name);
				free(array[i].price);
				free(array[i].profit);
    }
    free(array); //Lopuksi vapautetaan vielä arrayn itsensä muisti
}

struct product *add_game(struct product *array, int size, char *string, float b)  {

  array = realloc(array, sizeof(struct product)*(size+1)); //Lisätään arrayhin yksi muistipaikka lisää
  if (array ==NULL)  {
    return NULL;
  }

  array[size].name = malloc(strlen(string)+1); //Varataan kaikille structin osille muisti ja sijoitetaan niihin arvot
  strcpy(array[size].name,string);

  array[size].price = malloc(sizeof(float));
  array[size].profit = malloc(sizeof(float));
  *array[size].price = b;
  *array[size].profit = 0;
	printf("Peli %s lisätty onnistuneesti taulukkoon.\n", array[size].name);
  return array; //Palautetaan uuden alkion saanut array
}

void tuote_myyty(struct product *array, int i, char *string, float b) {
  int j=0;
  while(( (j < i) && strcmp(array[j].name,string)!=0)) { //Katsotaan lista läpi löytyykö samannimistä peliä
    j++;
  }
  if (j == i) {
    printf("Tuotetta ei löytynyt\n");
    return;
  }
  else  {
    *array[j].profit = *array[j].profit + b*(*array[j].price);
		printf("Tuotteen %s tuotto kasvoi %.2f. Peli on tuottanut yhteensä %.2f.\n", array[j].name, (b*(*array[j].price)), *array[j].profit);
  }
}

struct product *jarjestely(struct product *array, int i)
{
  struct product temp; //Väliaikainen sijoituspaikka
  for(int k=0;k<i;k++)  { //Käydään läpi lista useaan kertaan, jotta lopulta kaikki on järjestelty
    for(int j=0;j<(i-1);j++) {
      if (*array[j].profit < *array[j+1].profit)  { //Jos jälkimmäinen on suurempi vaihdetaan peräkkäisten alkioiden paikkaa
        temp = array[j];
        array[j] = array[j+1];
        array[j+1]=temp;
      }
    }
  }
  return array; //Palautetaan järjestelty array
}

void print_games(struct product *array, int i)  {
  array = jarjestely(array,i); //Järjestellään array
	printf("Pelin nimi \t Pelin Hinta \t Tuotto\n");
  for(int j=0;j<i;j++)  {
		printf("%-10s \t %-6.2f \t %-6.2f\n", array[j].name, *array[j].price, *array[j].profit);
    //printf("Nimi: %-10s \t Hinta: %-6.2f \t Tuotto: %-6.2f\n", array[j].name, *array[j].price, *array[j].profit); //Tulostetaan järjestetty array
  }
}

void tallenna_tiedostoon(char *filename, struct product *array, int i) {
  FILE *f = fopen(filename,"w");

  if(!f)  {
    printf("Tiedoston avaamisessa tapahtui virhe.\n");
    return;
  }
  for(int j = 0; j < i; j++){
    fprintf(f,"%s %.2f %.2f \n", array[j].name, *array[j].price, *array[j].profit); //Tulostetaan kaikki alkiot tiedostoon
}
fclose(f);
printf("Tuotteiden tallentaminen tiedostoon onnistui.\n");
}

int laske_rivit(FILE *f) {
  char merkki;
  int rivi = 0;
  while ((merkki = fgetc(f)) != EOF)	{
        if (merkki == '\n') //Rivinvaihdosta lisätään rivi.
            rivi++;
    }

    return rivi;
}

struct product *lataa_tiedot(char *filename, struct product *array, int j) {
  muistinnollaus(array,j); //Tyhjennetään vanha array
  FILE *f = fopen(filename, "r");
  if(!f)  {
    printf("Tiedoston avaamisessa tapahtui virhe.");
    return 0;
  }
  int rivit = laske_rivit(f); //Lasketaan arrayn alkioiden määrä
  rewind(f);
  struct product *new_array = malloc((rivit + 1) * sizeof(struct product)); //Varataan muistia
  //array = realloc(array, (rivit + 2) * sizeof(struct product));
  char name[50];
  float price;
  float profit;

  for (int i=0;i<rivit;i++){
    fscanf(f, "%s %f %f",  name, &price, &profit); //Tulostetaan tiedot tiedostosta omiin muuttujiinsa

    new_array[i].name = malloc(strlen(name)+1); //Varataan muistia ja sijoitetaan arvot
    strcpy(new_array[i].name,name);

    new_array[i].price = malloc(sizeof(float));
    new_array[i].profit = malloc(sizeof(float));
    *new_array[i].price = price;
    *new_array[i].profit = profit;
  }
  fclose(f);
  printf("Pelien tiedot ladattu tiedostosta.\n");
  return new_array; //Palautetaan uusi array
}


int main(void) {
  char a[100];
  char string[20];
  char input[100];
  float number;
  int amount;
  int i = 0;
  int c=0;
  struct product *array = malloc(sizeof(struct product)); //Luodaan array
  while(c==0)  {
    fgets(input, 1000, stdin); //Syöte käyttäjältä
    sscanf(input,"%s %s", a, string); //Katsotaan käyttäjän komento

    switch(a[0]) { //Katsotaan seuraava toimenpide
      case 'A':
        if(sscanf(input,"%s %s %f",a, string, &number)==3)  { //Erotetaan syötteestä kaikki arvot, tarkistetaan syötteen oikeellisuus
          array = add_game(array, i, string, number);
					if(array==NULL)	{
						printf("Pelin lisääminen epäonnistui.\n");
					}
					i++;
        }
        else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      case 'B':
        if(sscanf(input,"%s %s %d",a, string, &amount)==3)  { //Erotetaan syötteestä kaikki arvot, tarkistetaan syötteen oikeellisuus
          tuote_myyty(array,i, string, amount);
        }
        else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      case 'L':
				if(sscanf(input,"%s",a)==1)	{
        	print_games(array,i);
				}
				else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      case 'W':
        if(sscanf(input,"%s %s",a, string)==2)  { //Erotetaan syötteestä kaikki arvot, tarkistetaan syötteen oikeellisuus
          tallenna_tiedostoon(string,array,i);
        }
        else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      case 'O':
        if(sscanf(input,"%s %s",a, string)==2)  { //Erotetaan syötteestä kaikki arvot, tarkistetaan syötteen oikeellisuus
					array = lataa_tiedot(string,array, i);

					FILE *f = fopen(string, "r");

					if(!f)  {
						printf("Tiedoston avaamisessa tapahtui virhe.\n");
						return 0;
					}
					//rewind(f);
					i = laske_rivit(f); //Muutetaan listan koko
					fclose(f);
        }
        else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      case 'Q':
				if(sscanf(input,"%s",a)==1)	{
        	muistinnollaus(array,i); //Tyhjennetään ohjelmassa varattu muisti
        	printf("Muisti nollattu, poistutaan ohjelmasta.\n");
        	c=1;
				}
				else  {
          printf("Syöte oli virheellinen.\n");
        }
        break;

      default:
        printf("Virheellinen komento.\n");
    }
  }
  return 0;
}
