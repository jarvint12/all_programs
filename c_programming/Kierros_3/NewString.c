#include <stdio.h>
#include <stddef.h>

void qstr_print(const char *s)  {
  int i=0;
  while(s[i] != '?')  {
    printf("%c", s[i]);
    i++;
  }
}

unsigned int qstr_length(const char *s) {
int i = 0;
  while(s[i] != '?')  {
    i++;
  }
  printf("%d", i);
  return i;
}

int qstr_cat(char *dst, char *src)  {
  int i = 0;
  int j = 0;
  while(dst[i]!='?')  {
    i++;
  }
  while(src[j]!='?')  {
    dst[i] = src[j];
    i++;
    j++;
  }
  dst[i] = '?';
  printf("%d",i);
  return i;
}


const char *qstr_strstr(const char *str1, const char *str2) {
  int i=0;
  int j=0;
  while(str1[i]!='?')  {
    while(str2[j]!='?') {
      if(str1[i]==str2[j])  {
        j++;
      }
      else  {
        i++;
        break;
      }
      i++;
    }
    if(str2[j]=='?')  {
      i = i-j;
      break;
    }
    else  {
      j = 0;
    }
  }
  if(str2[j]=='?')  {
    return &str1[i];
  }
  else  {
    return NULL;
  }
}

int main(void)  {
  qstr_print("Auto ajoi?kilparataa");
  qstr_length("Auto ajoi?kilparataa");
  char dst[50] = "Auto ajoi?";
  char *src = " tietä pitkin? lujaa";
  qstr_cat(dst,src);
  char *str1 = "Auto ajoi tietä pitkin";
  char *str2 = "tie";
  qstr_strstr(str1,str2);
  return 0;
}
