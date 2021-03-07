import pandas as pd
import re


# define custom functions

def apply_manual_fixes(data):
    data[0][1401] = '\xa0\xa0\xa0Andrena takachihoi\xa0Hirashima, 1964, emend.' \
                    '\xa0--\xa0Andrena (Euandrena) takachihsi\xa0' \
                    'Hirashima, 1964, incorrect original spelling in species heading'
    return data


def read_data(names_file):
    df = pd.read_csv(names_file, header=None)
    return df


def write_data(data, output_file):
    data_out = pd.DataFrame(data)
    data_out.to_csv(output_file, encoding='utf-8-sig')


def flatten(mylist):
    rt = []
    for i in mylist:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i)
    return rt


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


def upper_repl(match):
    return match.group(1).upper()


def lower_repl(match):
    return match.group(1).lower()


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
        # if subspecies_exists and len(subspecies_exists[0].split(' ')) == 1:
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
    if mypub:  # if a publication was passed
        year_exists = re.search(r'[0-9][0-9][0-9][0-9]', mypub)  # find position of year, if it exists
        if year_exists:  # if a year exists in publication
            year_start_index = year_exists.span()[0]
            year_end_index = year_exists.span()[1]
            year_out = mypub[year_start_index:year_end_index]
            bracketed_date_exists = re.search(rf'\[{year_out}\]', mypub)
            mypub = mypub.replace('[', '').replace(']', '')
            if bracketed_date_exists:
                bracketed_date_out = True
                year_out_print = f'[{year_out}]'
                year_start_index -= 1
            else:
                bracketed_date_out = False
                year_out_print = year_out
            publication_notes_out = '; '.join([x.strip() for x in mypub[year_end_index:].split(',') if x])
            authors_exist = mypub[0:year_start_index].strip()
        else:  # a year is not in the publication
            year_out = '????'
            year_out_print = '????'
            publication_notes_exist = re.search(r', [a-z].*?$', mypub)  # notes are typically ', [a-z][a-z]...'
            if publication_notes_exist:
                publication_notes_out = '; '.join([x.strip() for x in publication_notes_exist[0].split(',') if x])
                year_start_index = publication_notes_exist.span()[0]
                authors_exist = re.sub(fr'{publication_notes_exist[0]}', '', mypub)
            else:
                publication_notes_out = ''
                year_start_index = len(mypub)
                authors_exist = True  # if no notes, no year, but pub exists, authors must exist
            bracketed_date_out = False
            year_separated_by_comma = True
        ### AUTHOR PARSING STARTS HERE
        if authors_exist:  # if an author string exists
            authors = mypub[0:year_start_index].strip()  # authors are publication string up to location of year
            authors = re.sub(r',$', r'', authors)  # remove trailing ','
            authors = re.sub(r'([A-Z])\.', r'\1. ', authors).replace('  ', ' ')  # put a space between initials
            if ' in ' in authors:
                extra_author_info = re.search(r'( in .*)', authors)[0]  # capture 'in ...' text separately
                if extra_author_info[0] != ' ':
                    extra_author_info = ' ' + extra_author_info
                if extra_author_info[-1] == ' ':
                    extra_author_info = extra_author_info[0:-1]
                authors = re.sub(extra_author_info, '', authors)
                extra_author_info = re.sub(r'\b( et al).*', ',\\1.', extra_author_info)  # ensure 'et al' is formatted
            else:
                extra_author_info = ''
            authors = re.sub(r' and | y | & ', r', ', authors)  # replace 'and', 'y', and '&' with ','
            authors = re.sub(r' PhD\.| Esq\.|, PhD\.|, Esq\.| MD\.| MS\.|, MD\.|, MS\.', r'', authors)  # remove honorary titles
            authors = re.sub(r',( Jr.*?| Sr.*?| I.*?| V.*?)$', r'\1', authors)  # protect generational titles
            if authors[-2:] in ['Jr', 'Sr']:  # ensure these titles end with '.'
                authors = authors + '.'
            authors = authors.replace(',,', ',')  # remove extra commas that may exist
            et_al_exists = re.search(r', et al*.?| et al*.?', authors)
            if et_al_exists:
                et_al_exists = True
                authors = re.sub(r', et al*.?| et al*.?', '', authors)
            ## Anticipated problem: ',' could separate names, initials, or titles like 'Lastname, Jr.', 'Lastname, III'
            if ',' in authors:  # if commas exist, we assume the names and initials are comma-separated
                author_list = [x.strip() for x in authors.split(',') if x]  # separate on commas, ignoring empty strings
            else:
                author_list = [authors]
            temp_author_list = []
            for author in author_list:  # CHECKS FOR ASA FORMATTED AUTHORS
                out_of_order = re.search(r' [A-Z]\.$| [A-Z]$', author)  # names end in trailing initials
                if out_of_order:  # if a name is out of order
                    previous_name = temp_author_list[-1]  # store previous name
                    temp_author_list = temp_author_list[0:-1]  # remove the previous name
                    new_name = author.strip() + ' ' + previous_name.strip()  # merge current name with previous name
                    temp_author_list.append(new_name)  # append new name to the list of authors
                else:  # if a name is not out of order
                    temp_author_list.append(author)  # append the name to the list of authors
            author_list = temp_author_list
            temp_author_list = []
            for author in author_list:  # CHECKS FOR APA FORMATTED AUTHORS
                # names containing initials ONLY
                out_of_order = re.search(r'^([A-Z]\.)+$|^([A-Z] )+$|^([A-Z]\. )+(?!.*[a-z])', author)
                if out_of_order:  # if a name is out of order
                    surname = temp_author_list[-1]  # store previous name
                    temp_author_list = temp_author_list[0:-1]  # remove the previous name
                    initials = re.sub(r'([A-Z])\.', '\\1. ', author)  # place '. ' between each initial
                    new_name = initials.strip() + ' ' + surname.strip()  # merge current name with previous name
                    temp_author_list.append(new_name)  # append new name to the list of authors
                else:  # if a name is not out of order
                    temp_author_list.append(author)  # append the name to the list of authors
            author_list = temp_author_list
            temp_author_list = []
            for author in author_list:  # CHECKS FOR AMA FORMATTED AUTHORS
                trailing = re.search(r'( Jr.*?| Sr.*?| I.*?| V.*?)$', author)
                if trailing:
                    suffix = author[trailing.span()[0]:trailing.span()[1]]
                    author = author[0:trailing.span()[0]]
                else:
                    suffix = ''
                out_of_order = re.search(r' [A-Z]+$', author)  # names end in multiple trailing initials
                if out_of_order:  # if a name is out of order
                    initials = ' '.join(author.split(' ')[1:])  # grab initials
                    initials = re.sub(r'([A-Z])', '\\1. ', initials)  # place '. ' between each initial
                    surname = author.split(' ')[0]  # grab surname
                    new_name = initials.strip() + ' ' + surname.strip() + suffix  # merge initials and surname
                    temp_author_list.append(new_name)  # append new name to the list of authors
                else:  # if a name does not contain elements out of order
                    temp_author_list.append(author + suffix)  # append the name to the list of authors
            author_list = temp_author_list
            number_of_authors = len(author_list)
            author_list = [re.sub(r'( Jr.*?| Sr.*?| I.*?| V.*?)$', ',\\1', x) for
                           x in author_list]  # comma-separate generational titles
            author_list_out = author_list
            author_list_display = [re.sub(r'(van |de |van de )', upper_repl, x) for x in  # protect prefixes from next
                                   author_list_out]  # (I couldn't figure out the correct regex for this)
            author_list_display = [re.sub(r'([a-z]+)(?!.*^) ', r'. ', x) for x in
                                   author_list_display]  # collapse non-surnames to an initial (does not handle prefix)
            author_list_display = [re.sub(r'(\. (?![A-Z][a-z])+)', r'.', x) for x in
                                   author_list_display]  # remove space between initials
            author_list_display = [re.sub(r'(VAN |DE |VAN DE )', lower_repl, x) for x in
                                   author_list_display]  # unprotect prefixes
            if et_al_exists:
                number_of_authors = 25  # arbitrarily large value to trigger 'et al' in citation_out
        else:  # if an author string does not exist
            number_of_authors = 0
            author_list_out = ['']
            author_list_display = ['']
        # GENERATE AUTHOR STRING TO DISPLAY IN OUTPUT
        if number_of_authors == 0:
            citation_out = 'Unknown, ' + year_out_print
        elif number_of_authors == 1:
            citation_out = author_list_display[0] + extra_author_info + ', ' + year_out_print
        elif number_of_authors == 2:
            citation_out = ', '.join(author_list_display[0:-1]) + ' and ' + author_list_display[
                -1] + extra_author_info + ', ' + year_out_print
        elif number_of_authors == 3:
            citation_out = ', '.join(author_list_display[0:-1]) + ', and ' + author_list_display[
                -1] + extra_author_info + ', ' + year_out_print
        else:
            citation_out = author_list_display[0] + ' et al.' + extra_author_info + ', ' + year_out_print  #
    else:
        author_list_out, year_out, citation_out, publication_notes_out, bracketed_date_out = [''], '', '', '', False
    return author_list_out, year_out, citation_out, publication_notes_out, bracketed_date_out


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
                              for x in note_out.split(' ')]). \
            replace('.', '').replace('sl', 'sensu lato').replace('homonytm', 'homonym')
        note_out = re.sub(r'homony$', 'homonym', note_out)
        note_out = re.sub(r'misdet', 'misidentification', note_out.replace('.', ''))
        name_out = name_in.split('_')[0].replace('_', ' ')
    else:
        name_out = name_in
        note_out = ''
    return name_out, note_out


def subspecies_prefix_cleaner(name_in):
    name_out = name_in.replace('.', '').replace(',', '').replace('var ', 'variety '). \
        replace('v ', 'variety ').replace('m ', 'morph ').replace('morpha ', 'morph '). \
        replace('f ', 'form ').replace('ab ', 'abberration '). \
        replace('aber ', 'abberration ').replace('aberr ', 'abberration '). \
        replace('r ', 'race ').replace('rasse ', 'race ').replace('mut ', 'mutant')
    # mod = ???  # not sure what 'mod' means, but it is present sometimes
    return name_out
