#ifndef AALTO_C_BOOK
#define AALTO_C_BOOK

// Date in numeric format
struct date {
    unsigned char day;
    unsigned char month;
    int year;
};

// Single book entry
struct book {
	char id[10];
	char *title;
	char *author;
	struct date release_date;
};


int init_book(struct book *p_book, const char *p_id, const char *p_title, const char * p_author, struct date p_release);

struct book *add_to_collection(struct book *collection, unsigned int size, struct book new_book);

#endif
