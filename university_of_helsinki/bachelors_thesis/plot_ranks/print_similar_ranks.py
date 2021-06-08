


def print_similar_ranks(top, m_top, d_top, o_top):
    in_all=list()
    in_dm=list()
    in_om=list()
    in_do=list()
    only_m=list()
    only_d=list()
    only_o=list()
    for i in range(len(m_top)):
        m_gene=m_top[i]
        d_gene=d_top[min(i,len(d_top)-1)]
        o_gene=o_top[i]
    #for m_gene, d_gene, o_gene in zip(m_top, d_top, o_top):
        if o_gene=="VWF":
            current=True
        else:
            current=False
        if m_gene in d_top and m_gene in o_top:
            if m_gene not in in_all:
                in_all.append(m_gene)
        elif m_gene in d_top:
            if m_gene not in in_dm:
                in_dm.append(m_gene)
        elif m_gene in o_top:
            if m_gene not in in_om:
                in_om.append(m_gene)
        else:
            if m_gene not in only_m:
                only_m.append(m_gene)
        if not (d_gene in m_top and d_gene in o_top):
            if d_gene in m_top:
                pass
            elif d_gene in o_top:
                if d_gene not in in_do:
                    in_do.append(d_gene)
            else:
                if d_gene not in only_d:
                    only_d.append(d_gene)
        if not (o_gene in m_top and o_gene in d_top):
            if current:
                print("Lapi1")
            if o_gene in m_top:
                if current:
                    print("muffinn?")
                    print(m_top)
                pass
            elif o_gene in d_top:
                if current:
                    print("dendrix?")
                pass
            else:
                if current:
                    print("LaPI2")
                if o_gene not in only_o:
                    if current:
                        print("LaPI3")
                    only_o.append(o_gene)

    print("\n"+top+":")
    print("In all: ",in_all)
    print("\nIn MUFFINN and Dendrix: ",in_dm)
    print("\nIn MUFFINN and Oncodrive-fm: ",in_om)
    print("\nIn Oncodrive-fm and Dendrix: ",in_do)
    print("\nOnly in MUFFINN : ",only_m)
    print("\nOnly in Dendrix : ",only_d)
    print("\nOnly in Oncodrive-fm : ",only_o)


def get_top_list(gene_list, number):
    top_list=list()
    for gene in gene_list:
        if len(top_list)<number:
            if not gene in top_list:
                top_list.append(gene)
        else:
            break
    return top_list

def get_list(file, nrow_header, genes_cols):
    genes=list()
    with open(file) as fr:
        for line in fr.readlines()[nrow_header:]:
            for col_gene in genes_cols:
                gene=line.split()[col_gene]
                genes.append(gene)
    return genes


def get_similar_ranks():
    directory="/csc/mustjoki2/variant_move/epi_ski/mutation_load_tool/re_permutation/real_results/"
    onco_file=directory+"gold-genes_sorted.tsv"
    dendrix_file=directory+"sets_weightOrder_experiment0.txt"
    muffinn_file=directory+"DNsum_gold.STRINGv10"
    muffinn_genes=get_list(muffinn_file, 1, [2])
    dendrix_genes=get_list(dendrix_file, 0, [1, 2, 3])
    onco_genes=get_list(onco_file, 1, [0])
    m_top5=get_top_list(muffinn_genes, 5)
    d_top5=get_top_list(dendrix_genes, 5)
    o_top5=get_top_list(onco_genes, 5)
    m_top10=get_top_list(muffinn_genes, 10)
    d_top10=get_top_list(dendrix_genes, 10)
    o_top10=get_top_list(onco_genes, 10)
    m_top50=get_top_list(muffinn_genes, 50)
    d_top50=get_top_list(dendrix_genes, 50)
    o_top50=get_top_list(onco_genes, 50)
    print_similar_ranks("Top5", m_top5, d_top5, o_top5)
    print_similar_ranks("Top10", m_top10, d_top10, o_top10)
    print_similar_ranks("Top50", m_top50, d_top50, o_top50)

def main():
    get_similar_ranks()


if __name__=='__main__':
    main()
