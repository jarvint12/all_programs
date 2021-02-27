#include <stdio.h>



int getSourcePort(const unsigned char *tcp_hdr) {
  unsigned int result = (tcp_hdr[0]<<8)|tcp_hdr[1];
  return result;
}

int getDestinationPort(const unsigned char *tcp_hdr)  {
  unsigned int result = (tcp_hdr[2]<<8)|tcp_hdr[3];
  return result;
}

void setSourcePort(unsigned char *tcp_hdr, int port)  {
  int port2 = port;
  port2 = port2 >> 8;
  port = port << 8;
  port = port >> 8;
  tcp_hdr[0] = port2;
  tcp_hdr[1] = port;
}
void setDestinationPort(unsigned char *tcp_hdr, int port) {
  int port2 = port;
  port2 = port2 >> 8;
  port = port << 8;
  port = port >> 8;
  tcp_hdr[2] = port2;
  tcp_hdr[3] = port;
}

int getAckFlag(const unsigned char *tcp_hdr)  {
  if(tcp_hdr[13]&0x10)  {
    return 1;
  }
  else  {
    return 0;
  }
}
void setAckFlag(unsigned char *tcp_hdr, int flag) {
  if (flag){
       tcp_hdr[13] = tcp_hdr[13] | (1 << 4);
  }
  else{
      tcp_hdr[13] = tcp_hdr[13] & ~(1 << 4);
  }
}

int getDataOffset(const unsigned char *tcp_hdr) {
  unsigned int result = tcp_hdr[12]>>4;
  return result;
}

void setDataOffset(unsigned char *tcp_hdr, int offset)  {
  int a = tcp_hdr[12];
  tcp_hdr[12] = 0x00;
  a = a << 4;
  a = a >> 4;
  tcp_hdr[12] = offset;
  tcp_hdr[12] = tcp_hdr[12] << 4;
  tcp_hdr[12] = tcp_hdr[12] | a;
}
