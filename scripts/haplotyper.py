import argparse
from utils import get_reverse_complement, parse_CIGAR

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-fs', '--fn_sam',
        help = 'input sam file for haplotyping'
    )
    parser.add_argument(
        '-pos', '--pos_interest',
        help = 'string contains the interested positions:\n \
                start with the chromosome name and follows by the positions\n \
                separated by colon. e.g. \"chr17:42451720:42453080\"'
    )
    parser.add_argument(
        '-fo', '--fo_tsv',
        help = 'output phasing tsv report file'
    )
    args = parser.parse_args()
    return args


def base_from_cigar(SEQ, cigar, pos_str, list_interest):
    number, operate = parse_CIGAR(cigar)
    ref_cursor = pos_str
    SEQ_cursor = 0
    
    interest_idx = 0
    haplotype = []
    for idx, op in enumerate(operate):
        if interest_idx >= len(list_interest):
            return haplotype
        num = number[idx]
        if op == 'M':
            ref_cursor += num
            SEQ_cursor += num
            if list_interest[interest_idx] < ref_cursor:
                while list_interest[interest_idx] < ref_cursor:
                    #print(list_interest[interest_idx], SEQ[SEQ_cursor - (ref_cursor - list_interest[interest_idx]) ])
                    haplotype.append((list_interest[interest_idx],SEQ[SEQ_cursor - (ref_cursor - list_interest[interest_idx]) ]))
                    interest_idx += 1
                    if interest_idx >= len(list_interest):
                        break
        elif op == 'D':
            ref_cursor += num
            SEQ_cursor
            if list_interest[interest_idx] < ref_cursor:
                while list_interest[interest_idx] < ref_cursor:
                    #print(list_interest[interest_idx], 'D(' + str(num) + ')')
                    haplotype.append((list_interest[interest_idx], 'D(' + str(num) + ')'))
                    interest_idx += 1
                    if interest_idx >= len(list_interest):
                        break
        elif op == 'I':
            ref_cursor
            SEQ_cursor += num
            if list_interest[interest_idx] == ref_cursor:
                #print(list_interest[interest_idx], 'I(' + SEQ[SEQ_cursor-num:SEQ_cursor] + ')')
                haplotype.append((list_interest[interest_idx],'I(' + SEQ[SEQ_cursor-num:SEQ_cursor] + ')'))
        elif op == 'H':
            pass
        elif op == 'S':
            ref_cursor
            SEQ_cursor += num
        else:
            print("CIGAR ERROR:", op)
    if len(haplotype) > 0:
        return haplotype




if __name__ == '__main__':
    args = parse_args()
    fn_sam = args.fn_sam
    pos_interest = args.pos_interest
    fo_tsv = args.fo_tsv

    chr_name = pos_interest.split(':')[0]
    list_interest = pos_interest.split(':')[1:]
    if len(list_interest) < 2:
        print("Number of interested position not enough for phasing!")
    list_interest = [int(pos) for pos in list_interest]

    dict_haplotype = {}
    # dict_haplotype {}
    # - keys: ['A', 'C', 'G']  // haplotype
    # - values: how many times the haplotype appears

    f_n = open(fn_sam, 'r')
    for line in f_n:
        if line[0] == '@':
            continue
        fields = line.split()
        if fields[2] != chr_name:
            continue
        pos_str = int(fields[3])
        if pos_str > list_interest[0]:
            continue
        name  = fields[0]
        cigar = fields[5]
        SEQ   = fields[9]
        haplotype = base_from_cigar(SEQ, cigar, pos_str, list_interest)
        if haplotype:
            haplotype = tuple(haplotype)
            if dict_haplotype.get(haplotype):
                dict_haplotype[haplotype] += 1
            else:
                dict_haplotype[haplotype] = 1
        
    f_n.close()

    f_o = open(fo_tsv, 'w')
    f_o.write("Phasing_of_" + chr_name + "_" + str(list_interest[0]) + "\n")
    f_o.write("Number\tPercent(%)")
    for pos in list_interest:
        f_o.write("\t")
        f_o.write(str(pos))
    total_num = sum([item[1] for item in dict_haplotype.items()])
    for pair, num in sorted(dict_haplotype.items(), key = lambda item: item[1] , reverse=True):
        f_o.write('\n' + str(num) + '\t' + "{:.2f}".format(num*100/total_num))
        old_pos = -1
        for item in pair:
            current_pos = item[0]
            SEQ = item[1]
            if current_pos != old_pos:
                f_o.write('\t')
            f_o.write(SEQ)
            old_pos = current_pos
    f_o.close()


