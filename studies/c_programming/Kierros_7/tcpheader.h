struct tcpHeader {
    unsigned short src_port;
    unsigned short dest_port;
    unsigned int seq_number;
    unsigned int acknowledgment;
    unsigned int offset;  // in bytes
    char ns;
    char cwr;
    char ece;
    char urg;
    char ack;
    char psh;
    char rst;
    char syn;
    char fin;
    unsigned int window;
    unsigned int checksum;
    unsigned int urg_ptr;
};

int getSourcePort(const unsigned char *tcp_hdr);
int getDestinationPort(const unsigned char *tcp_hdr);
void setSourcePort(unsigned char *tcp_hdr, int port);
void setDestinationPort(unsigned char *tcp_hdr, int port);
int getAckFlag(const unsigned char *tcp_hdr);
void setAckFlag(unsigned char *tcp_hdr, int flag);
int getDataOffset(const unsigned char *tcp_hdr);
void setDataOffset(unsigned char *tcp_hdr, int offset);
