import pandas as pd
import re

names_file = 'input/bee_names.csv'
names_output_file = 'output/bee_names_extracted.csv'
author_output_file = 'output/bee_authors_extracted.csv'
log_file = 'output/log_file.csv'

pLu = "[A-Z\u00C0-\u00D6\u00D8-\u00DE\u0100\u0102\u0104\u0106\u0108\u010A\u010C\u010E\u0110\u0112\u0114\u0116\u0118" \
      "\u011A\u011C\u011E\u0120\u0122\u0124\u0126\u0128\u012A\u012C\u012E\u0130\u0132\u0134\u0136\u0139\u013B\u013D" \
      "\u013F\u0141\u0143\u0145\u0147\u014A\u014C\u014E\u0150\u0152\u0154\u0156\u0158\u015A\u015C\u015E\u0160\u0162" \
      "\u0164\u0166\u0168\u016A\u016C\u016E\u0170\u0172\u0174\u0176\u0178\u0179\u017B\u017D\u0181\u0182\u0184\u0186" \
      "\u0187\u0189-\u018B\u018E-\u0191\u0193\u0194\u0196-\u0198\u019C\u019D\u019F\u01A0\u01A2\u01A4\u01A6\u01A7" \
      "\u01A9\u01AC\u01AE\u01AF\u01B1-\u01B3\u01B5\u01B7\u01B8\u01BC\u01C4\u01C7\u01CA\u01CD\u01CF\u01D1\u01D3\u01D5" \
      "\u01D7\u01D9\u01DB\u01DE\u01E0\u01E2\u01E4\u01E6\u01E8\u01EA\u01EC\u01EE\u01F1\u01F4\u01F6-\u01F8\u01FA\u01FC" \
      "\u01FE\u0200\u0202\u0204\u0206\u0208\u020A\u020C\u020E\u0210\u0212\u0214\u0216\u0218\u021A\u021C\u021E\u0220" \
      "\u0222\u0224\u0226\u0228\u022A\u022C\u022E\u0230\u0232\u023A\u023B\u023D\u023E\u0241\u0243-\u0246\u0248\u024A" \
      "\u024C\u024E\u0370\u0372\u0376\u037F\u0386\u0388-\u038A\u038C\u038E\u038F\u0391-\u03A1\u03A3-\u03AB\u03CF" \
      "\u03D2-\u03D4\u03D8\u03DA\u03DC\u03DE\u03E0\u03E2\u03E4\u03E6\u03E8\u03EA\u03EC\u03EE\u03F4\u03F7\u03F9" \
      "\u03FA\u03FD-\u042F\u0460\u0462\u0464\u0466\u0468\u046A\u046C\u046E\u0470\u0472\u0474\u0476\u0478\u047A" \
      "\u047C\u047E\u0480\u048A\u048C\u048E\u0490\u0492\u0494\u0496\u0498\u049A\u049C\u049E\u04A0\u04A2\u04A4\u04A6" \
      "\u04A8\u04AA\u04AC\u04AE\u04B0\u04B2\u04B4\u04B6\u04B8\u04BA\u04BC\u04BE\u04C0\u04C1\u04C3\u04C5\u04C7\u04C9" \
      "\u04CB\u04CD\u04D0\u04D2\u04D4\u04D6\u04D8\u04DA\u04DC\u04DE\u04E0\u04E2\u04E4\u04E6\u04E8\u04EA\u04EC\u04EE" \
      "\u04F0\u04F2\u04F4\u04F6\u04F8\u04FA\u04FC\u04FE\u0500\u0502\u0504\u0506\u0508\u050A\u050C\u050E\u0510\u0512" \
      "\u0514\u0516\u0518\u051A\u051C\u051E\u0520\u0522\u0524\u0526\u0528\u052A\u052C\u052E\u0531-\u0556\u10A0-" \
      "\u10C5\u10C7\u10CD\u13A0-\u13F5\u1E00\u1E02\u1E04\u1E06\u1E08\u1E0A\u1E0C\u1E0E\u1E10\u1E12\u1E14\u1E16\u1E18" \
      "\u1E1A\u1E1C\u1E1E\u1E20\u1E22\u1E24\u1E26\u1E28\u1E2A\u1E2C\u1E2E\u1E30\u1E32\u1E34\u1E36\u1E38\u1E3A\u1E3C" \
      "\u1E3E\u1E40\u1E42\u1E44\u1E46\u1E48\u1E4A\u1E4C\u1E4E\u1E50\u1E52\u1E54\u1E56\u1E58\u1E5A\u1E5C\u1E5E\u1E60" \
      "\u1E62\u1E64\u1E66\u1E68\u1E6A\u1E6C\u1E6E\u1E70\u1E72\u1E74\u1E76\u1E78\u1E7A\u1E7C\u1E7E\u1E80\u1E82\u1E84" \
      "\u1E86\u1E88\u1E8A\u1E8C\u1E8E\u1E90\u1E92\u1E94\u1E9E\u1EA0\u1EA2\u1EA4\u1EA6\u1EA8\u1EAA\u1EAC\u1EAE\u1EB0" \
      "\u1EB2\u1EB4\u1EB6\u1EB8\u1EBA\u1EBC\u1EBE\u1EC0\u1EC2\u1EC4\u1EC6\u1EC8\u1ECA\u1ECC\u1ECE\u1ED0\u1ED2\u1ED4" \
      "\u1ED6\u1ED8\u1EDA\u1EDC\u1EDE\u1EE0\u1EE2\u1EE4\u1EE6\u1EE8\u1EEA\u1EEC\u1EEE\u1EF0\u1EF2\u1EF4\u1EF6\u1EF8" \
      "\u1EFA\u1EFC\u1EFE\u1F08-\u1F0F\u1F18-\u1F1D\u1F28-\u1F2F\u1F38-\u1F3F\u1F48-\u1F4D\u1F59\u1F5B\u1F5D\u1F5F" \
      "\u1F68-\u1F6F\u1FB8-\u1FBB\u1FC8-\u1FCB\u1FD8-\u1FDB\u1FE8-\u1FEC\u1FF8-\u1FFB\u2102\u2107\u210B-\u210D" \
      "\u2110-\u2112\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u2130-\u2133\u213E\u213F\u2145\u2160-\u216F" \
      "\u2183\u24B6-\u24CF\u2C00-\u2C2E\u2C60\u2C62-\u2C64\u2C67\u2C69\u2C6B\u2C6D-\u2C70\u2C72\u2C75\u2C7E-\u2C80" \
      "\u2C82\u2C84\u2C86\u2C88\u2C8A\u2C8C\u2C8E\u2C90\u2C92\u2C94\u2C96\u2C98\u2C9A\u2C9C\u2C9E\u2CA0\u2CA2\u2CA4" \
      "\u2CA6\u2CA8\u2CAA\u2CAC\u2CAE\u2CB0\u2CB2\u2CB4\u2CB6\u2CB8\u2CBA\u2CBC\u2CBE\u2CC0\u2CC2\u2CC4\u2CC6\u2CC8" \
      "\u2CCA\u2CCC\u2CCE\u2CD0\u2CD2\u2CD4\u2CD6\u2CD8\u2CDA\u2CDC\u2CDE\u2CE0\u2CE2\u2CEB\u2CED\u2CF2\uA640\uA642" \
      "\uA644\uA646\uA648\uA64A\uA64C\uA64E\uA650\uA652\uA654\uA656\uA658\uA65A\uA65C\uA65E\uA660\uA662\uA664\uA666" \
      "\uA668\uA66A\uA66C\uA680\uA682\uA684\uA686\uA688\uA68A\uA68C\uA68E\uA690\uA692\uA694\uA696\uA698\uA69A\uA722" \
      "\uA724\uA726\uA728\uA72A\uA72C\uA72E\uA732\uA734\uA736\uA738\uA73A\uA73C\uA73E\uA740\uA742\uA744\uA746\uA748" \
      "\uA74A\uA74C\uA74E\uA750\uA752\uA754\uA756\uA758\uA75A\uA75C\uA75E\uA760\uA762\uA764\uA766\uA768\uA76A\uA76C" \
      "\uA76E\uA779\uA77B\uA77D\uA77E\uA780\uA782\uA784\uA786\uA78B\uA78D\uA790\uA792\uA796\uA798\uA79A\uA79C\uA79E" \
      "\uA7A0\uA7A2\uA7A4\uA7A6\uA7A8\uA7AA-\uA7AE\uA7B0-\uA7B4\uA7B6\uFF21-\uFF3A\U00010400-\U00010427\U000104B0-" \
      "\U000104D3\U00010C80-\U00010CB2\U000118A0-\U000118BF\U0001D400-\U0001D419\U0001D434-\U0001D44D\U0001D468-" \
      "\U0001D481\U0001D49C\U0001D49E\U0001D49F\U0001D4A2\U0001D4A5\U0001D4A6\U0001D4A9-\U0001D4AC\U0001D4AE-" \
      "\U0001D4B5\U0001D4D0-\U0001D4E9\U0001D504\U0001D505\U0001D507-\U0001D50A\U0001D50D-\U0001D514\U0001D516-" \
      "\U0001D51C\U0001D538\U0001D539\U0001D53B-\U0001D53E\U0001D540-\U0001D544\U0001D546\U0001D54A-\U0001D550" \
      "\U0001D56C-\U0001D585\U0001D5A0-\U0001D5B9\U0001D5D4-\U0001D5ED\U0001D608-\U0001D621\U0001D63C-\U0001D655" \
      "\U0001D670-\U0001D689\U0001D6A8-\U0001D6C0\U0001D6E2-\U0001D6FA\U0001D71C-\U0001D734\U0001D756-\U0001D76E" \
      "\U0001D790-\U0001D7A8\U0001D7CA\U0001E900-\U0001E921\U0001F130-\U0001F149\U0001F150-\U0001F169\U0001F170-" \
      "\U0001F189]"

data = pd.read_csv(names_file, header=None)

# these lines are broken in the input file; requires manual fix
data[0][1401] = '\xa0\xa0\xa0Andrena takachihoi\xa0Hirashima, 1964, emend.' \
                '\xa0--\xa0Andrena (Euandrena) takachihsi\xa0' \
                'Hirashima, 1964, incorrect original spelling in species heading'


# define custom functions


def unicode_name_fix(line_in, parent_id_in):
    line_out = line_in.replace('ůoziůski', 'Ůoziůski')
    line_out = line_out.replace('_cincta', ' cincta')
    line_out = line_out.replace('Azorae', 'azorae')
    line_out = line_out.replace(' Evylaeus)', '\xa0Lasioglossum (Evylaeus)')
    line_out = line_out.replace(' Dialictus)', '\xa0Lasioglossum (Dialictus)')
    line_out = line_out.replace(' Austronomia)', '\xa0Lipotriches (Austronomia)')
    line_out = line_out.replace('\xa0Hedicke, 1938, Andrena ', '\xa0Hedicke, 1938;\xa0Andrena ')
    line_out = line_out.replace('Michener, 1966, Compsomelissa', 'Michener, 1966;\xa0Compsomelissa')
    line_out = line_out.replace('Andrena cingulata auct , not Fabricius', 'Andrena cingulata_auct,_not_Fabricius')
    line_out = line_out.replace('argentata auct, not Fabricius, 1793', 'argentata_auct_not_Fabricius,_1793')
    line_out = line_out.replace('subspecies Dieunomia', 'subspecies;\xa0Dieunomia')

    # log which lines got changed for manual verification!
    if line_out != line_in:
        log_out = {
            'parent_id': parent_id_in,
            'original_text': line_in,
            'altered_text': line_out
        }
    else:
        log_out = {
            'parent_id': '',
            'original_text': '',
            'altered_text': ''
        }
    line_out = line_out.replace('\xa0', ' ')
    return line_out, log_out


def genus_extractor(record):
    genus_out = [x for x in record.split(' ') if re.match(r'^[A-Z]', x)][0]
    return genus_out


def species_extractor(record):
    species_exists = [x for x in record.split(' ') if re.match(r'^[a-z]', x) or
                      re.search(r'^[A-Z]-', x) or re.search(r'^[0-9]-', x)]
    species_exists = [x for x in species_exists if '(' not in x and ')' not in x]  # handles (Subgenus [text])
    if species_exists:
        species_out = species_exists[0]
    else:
        species_out = ''
    return species_out


def subspecies_extractor(species_in, record):
    subspecies_exists = re.findall(fr'{species_in} (.*?) [A-Z]', record)
    subspecies_exists = [x for x in subspecies_exists if not re.search(r',$|^[A-Z]|and', x)]
    if subspecies_exists:
    #if subspecies_exists and len(subspecies_exists[0].split(' ')) == 1:
        subspecies_out = subspecies_exists[0].replace('(', '').replace(')', '')
    elif subspecies_exists:
        subspecies_out = ''  # not sure how to handle something like: 'Andrena cingulata auct , not Fabricius'
    else:
        subspecies_out = ''
    return subspecies_out


def subgenus_extractor(genus_in, species_in, record):
    subgenus_exists = re.findall(fr'{genus_in} (.*?) {species_in}', record)
    if subgenus_exists:
        subgenus_out = subgenus_exists[0].replace('(', '').replace(')', '')
        # if contains 'sl' change to a subgenus note of 'sensu latu'
        if ' sl' in subgenus_out:
            subgenus_out = subgenus_out.replace(' sl', '_sl')
    else:
        subgenus_out = ''
    return subgenus_out


def publication_extractor(record):
    publication_exists = [x for x in record.split(' ') if re.match(r'^\(|[A-Z]', x) and ')' not in x]
    if len(publication_exists) > 1:
        publication_start = publication_exists[1]
        publication_out = record[record.index(publication_start):].replace('(', '').replace(')', '').strip()
    else:
        publication_out = ''
    return publication_out


def publication_parser(mypub):
    # PASS: mypub = 'C.D. Author, 2000'
    # PASS: mypub = 'C.D. Author'
    # PASS: mypub = '1999'
    # PASS: mypub = '1999, note'
    # PASS: mypub = 'C.D. Author, note'
    # PASS: mypub = 'ABC Author and DE Author, 2000'
    # PASS: mypub = 'ABC Author y DE Author, 2000'
    # PASS: mypub = 'ABC Author & DE Author, 2000'
    # PASS: mypub = 'Author, A Author and B Author, 2000'
    # PASS: mypub = 'A Author B Author C Author, 2000'
    # PASS: mypub = 'A B Author, CD Author, Nick Dowdy, 2000, first note, second note'
    # PASS: mypub = 'A B Author, CD Author, Nick J. Dowdy, 2000, first note, second note'
    # PASS: mypub = 'Authora Authorb and Authorc, 2000, note'
    # PASS: mypub = "de Bruin, Dowdy, van de Kamp, van O'Brian, 2000"
    # PASS: mypub = "de Bruin Dowdy van de Kamp van O'Brian, 2000"
    # FAIL: mypub = 'Lastname, AB, CD Lastname, and EF Lastname, 2000, note1, note2'
    # FAIL: mypub = 'Lastname, AB, Lastname C.D., Lastname E.F, 2000, note1, note2'
    # FAIL: mypub = 'Lastname, AB  Lastname C.D.  Lastname E.F, 2000, note1, note2'

    if mypub:
        mypub.replace(' ', '').replace('.', '')  # combine everything
        year_exists = re.search(r'[0-9][0-9][0-9][0-9]', mypub)  # find position of year, if it exists
        if year_exists:
            year_start_index = year_exists.span()[0]
            year_end_index = year_exists.span()[1]
            year_out = mypub[year_start_index:year_end_index]
            publication_notes_out = '; '.join([x.strip() for x in mypub[year_end_index:].split(',') if x])
        else:
            year_out = '????'
            publication_notes_exist = re.search(r', [a-z].*?$', mypub)  # notes are typically ', [a-z][a-z]...'
            if publication_notes_exist:
                publication_notes_out = '; '.join([x.strip() for x in publication_notes_exist[0].split(',') if x])
                year_start_index = publication_notes_exist.span()[0]
            else:
                publication_notes_out = ''
                year_start_index = len(mypub)
        authors = mypub[0:year_start_index]
        space_sep_authors = [x for x in authors.replace(', ', '').split(' ') if x not in ['and', '&', 'y']]
        names2 = [x for x in space_sep_authors if re.search(r"^[A-z]([^A-Z]| [A-Z]|'[A-Z])*?[a-z]$", x)]
        single_name_authors_only = len(names2) - len(space_sep_authors)
        if single_name_authors_only == 0:
            author_list_out = space_sep_authors
            # combine 'van' and 'de' with next word, until added to a word starting with [A-Z]
            author_list_out = [re.sub(r'\s+', ' ', x).strip() for x in ''.join(
                ['!' if x == 'van' else '@' if x == 'de' else x + ';' for x in
                 author_list_out]).replace('@', ' de ').replace('!', ' van ').strip().split(';') if x]
        else:
            authors = re.sub(r', $', '', authors)
            if ',' not in authors:
                test = [x.capitalize() if re.match(r'^[a-zA-Z]$', x) else x for x in space_sep_authors]
                if any([re.match(r'^[A-Z]$', x) for x in test]):  # if any test are single letter only
                    authors = ''.join([x.capitalize() if re.match(r'^[a-zA-Z]$', x) else x for x in space_sep_authors])
                    authors = re.sub(r'([a-z])([A-Z][a-zA-z])', '\\1, \\2', authors)
            comma_sep_authors = authors.replace(' and ', ', ').replace(' y ', ', ').replace(' & ', ', ').split(',')
            author_list_out = [x.replace(',', '').strip() for x in comma_sep_authors if x.replace(',', '').replace(' ', '')]
            unseparated_authors_exists = [re.findall(r'[A-Z][A-Z]([a-z]*?)[a-z][A-Z]', x) for x in author_list_out]  # unseparated means AuthorAuthor
            if any(unseparated_authors_exists):
                author_list_out = [re.findall(r'.*?[a-z](?=(?:[A-Z])|$)', x.strip()) for x in author_list_out][0]
            author_list_out = [re.sub(r"([a-z])\. ", "\\1 ", re.sub(r'^\. ', '', re.sub(r"([A-Z])", ". \\1", x).strip().replace('..', '.'))) for x in author_list_out]
        number_of_authors = len(author_list_out)
        author_list_out = [re.sub(r'([A-Z]\.)([A-Z]\.) ', '\\1 \\2 ', re.sub(r'([a-z])\. ', '\\1 ', x.replace('. . ', '. ').replace(' . ', '. ').replace("'. ", "' "))) for x in author_list_out]
        if number_of_authors == 0:
            citation_out = 'Unknown, ' + year_out
        elif number_of_authors == 1:
            citation_out = author_list_out[0] + ', ' + year_out
        elif number_of_authors == 2:
            citation_out = author_list_out[0] + ' and ' + author_list_out[1] + ', ' + year_out
        else:
            citation_out = ', '.join(author_list_out[0:-1]) + ', and ' + author_list_out[-1] + ', ' + year_out
    else:
        author_list_out, year_out, citation_out, publication_notes_out = '', '', '', ''
    return author_list_out, year_out, citation_out, publication_notes_out


def old_publication_parser(mypub):
    if mypub:
        mypub_words = [x.strip() for x in mypub.split(' ')]
        year_exists = [x for x in mypub_words if re.search(r'[0-9][0-9][0-9][0-9]', x)]
        if year_exists:
            year_index = mypub_words.index(year_exists[0])
            # author_list_out currently doesnt handle: Author *et al.*, XXXX
            author_list_out = [encoding_fix(x.strip().replace(',', '').replace('(', '').replace(')', '')) for x in
                               mypub_words[0:year_index] if x != 'and' and x != '&' and x != 'y']
            author_list_out = [x for x in author_list_out if
                               re.match(r'^[A-Z](.*?)[A-Z]$', x.replace('.', '').replace(' ', ''))]
            year_out = mypub_words[year_index].strip().replace(',', '').replace('(', '').replace(')', '')
            publication_notes_out = '; '.join(
                [x.strip().replace(',', '') for x in ' '.join(mypub_words[year_index + 1:]).split(',')])
            number_of_authors = len(author_list_out)
            if number_of_authors == 0:
                citation_out = 'Unknown,' + year_out
            elif number_of_authors == 1:
                citation_out = author_list_out[0] + ', ' + year_out
            elif number_of_authors == 2:
                citation_out = author_list_out[0] + ' and ' + author_list_out[1] + ', ' + year_out
            else:
                citation_out = ', '.join(author_list_out[0:-1]) + ', and ' + author_list_out[-1] + ', ' + year_out
        else:
            author_list_out = [encoding_fix(x.strip().replace(',', '').replace('(', '').replace(')', '')) for x in mypub_words if
                               re.search(r'^' + pLu, x)]
            year_out = ''
            last_author_index = [idx for idx, s in enumerate(mypub_words) if author_list_out[-1] in s][-1]
            publication_notes_out = '; '.join(
                [x.strip().replace(',', '') for x in ' '.join(mypub_words[last_author_index + 1:]).split(',')])
            number_of_authors = len(author_list_out)
            if number_of_authors == 0:
                citation_out = 'Unknown, ????'
            elif number_of_authors == 1:
                citation_out = author_list_out[0] + ', ????'
            elif number_of_authors == 2:
                citation_out = author_list_out[0] + ' and ' + author_list_out[1] + ', ????'
            else:
                citation_out = ', '.join(author_list_out[0:-1]) + ', and ' + author_list_out[-1] + ', ????'
    else:
        author_list_out, year_out, citation_out, publication_notes_out = '', '', '', ''
    return author_list_out, year_out, citation_out, publication_notes_out


def to_canonical(genus_in, species_in):
    return ' '.join([genus_in.strip(), species_in.strip()])


def encoding_fix(author_in):
    author_out = re.sub(r'Reb.lo', 'Rebêlo', author_in)
    author_out = re.sub(r'Sep.lveda', 'Sepúlveda', author_out)
    author_out = re.sub(r'Qui.onez', 'Quiñonez', author_out)
    author_out = re.sub(r'J.nior', 'Júnior', author_out)
    author_out = re.sub(r'Y..ez', 'Yáñez', author_out)
    author_out = re.sub(r'Ord..ez', 'Ordóñez', author_out)
    return author_out


def name_note_extractor(name_in):
    if '_' in name_in:
        note_out = '_'.join([x.strip() for x in name_in.split('_')[1:]])
        # remove numbers from name notes (these are probably citation numbers?)
        # resolve some common abbreviated notes
        note_out = '; '.join([re.sub(r'[a-z][0-9]$', '', x).
                             replace('sic.', 'sic').
                             replace('.', '').replace('auct', 'auctorum')
                              for x in note_out.split(' ')]).\
            replace('.', '').replace('sl', 'sensu lato').replace('homonytm', 'homonym')
        note_out = re.sub(r'homony$', 'homonym', note_out)
        note_out = re.sub(r'misdet', 'misidentification', note_out.replace('.', ''))
        name_out = name_in.split('_')[0].replace('_', ' ')
    else:
        name_out = name_in
        note_out = ''
    return name_out, note_out


def subspecies_prefix_cleaner(name_in):
    name_out = name_in.replace('.', '').replace(',', '').replace('var ', 'variety ').\
        replace('v ', 'variety ').replace('m ', 'morph ').replace('morpha ', 'morph ').\
        replace('f ', 'form ').replace('ab ', 'abberration ').\
        replace('aber ', 'abberration ').replace('aberr ', 'abberration ').\
        replace('r ', 'race ').replace('rasse ', 'race ').replace('mut ', 'mutant')
    # mod = ???  # not sure what 'mod' means, but it is present sometimes
    return name_out


# define temp structures and variables
name_attributes = {}  # each name will be a dictionary
names_out_list = []  # all name dictionary will be stored in a list
running_author_list = []  # keeping track of all authors to generate author list
name_id = 1  # name index
accepted_genus = ''  # placeholder value
accepted_species = ''  # placeholder value
accepted_canonical_name = ''  # placeholder value
family = ''  # first line in data should be first family
# i = 1  # loop counter
change_log = []

for line in data[0]:
    # print(i)
    if '\xa0' in line:
        parent_id, original_parent_id = name_id, name_id
        parsed, log_result = unicode_name_fix(line, parent_id)
        if log_result['parent_id'] != '':
            change_log.append(log_result)
        names = re.split("--|; ", parsed)  # create list of names
        # name = names[0]  # testing helper
        status = 'accepted'
        for name in names:
            genus, genus_notes = name_note_extractor(genus_extractor(name))
            species, species_notes = name_note_extractor(species_extractor(name))
            subgenus, subgenus_notes = name_note_extractor(subgenus_extractor(genus, species, name))
            subspecies, subspecies_notes = name_note_extractor(subspecies_extractor(species, name))  # TODO: Still failing in multi-authored names, author strings with 'and', 'var',
            canonical_name = to_canonical(genus, species)
            pub_data = publication_extractor(name)
            author_list, year, citation, publication_notes = publication_parser(
                pub_data)  # TODO: Some authors are weird and need to be checked; encoding problems exist
            # if publication_notes contains 'valid subspecies', raise status to 'accepted'
            accepted_subspecies = ''
            if 'valid subspecies' in publication_notes:
                status = 'accepted'
                accepted_subspecies = subspecies
                parent_id = name_id
            if status == 'accepted':
                accepted_genus = genus
                accepted_species = species
                accepted_canonical_name = canonical_name
            name_attributes = {
                'name_id': name_id,
                'parent_id': parent_id,
                'status': status,
                'family': family,
                'accepted_genus': accepted_genus,
                'accepted_species': accepted_species,
                'accepted_subspecies': accepted_subspecies,
                'subgenus': subgenus,
                'genus': genus,
                'species': species,
                'subspecies': subspecies,
                'accepted_canonical_name': accepted_canonical_name,
                'canonical_name': canonical_name,
                'genus_notes': genus_notes,
                'subgenus_notes': subgenus_notes,
                'species_notes': species_notes,
                'subspecies_notes': subspecies_notes,
                'publication': citation,
                'publication_notes': publication_notes,
                'verbatim_name': name.strip(),
                'source': 'Discover Life'
            }
            names_out_list.append(name_attributes)
            if author_list:
                running_author_list = list(set(running_author_list + author_list))
            parent_id = original_parent_id
            status = 'synonym'
            name_id += 1
    else:
        family = line.strip()
#    i += 1

# write out
names_data_out = pd.DataFrame(names_out_list)
names_data_out.to_csv(names_output_file, encoding='utf-8-sig')

running_author_list.sort()
author_data_out = pd.DataFrame(running_author_list)
author_data_out.to_csv(author_output_file, encoding='utf-8-sig')

log_data_out = pd.DataFrame(change_log)
log_data_out.to_csv(log_file, encoding='utf-8-sig')
