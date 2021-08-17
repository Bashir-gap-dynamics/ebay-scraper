import re


 
def data_read_lst():
    r_lst_ref = []

    # open file and read the content in a list
    stringline = ""
    with open('text.txt', 'r') as filehandle:
        count = 0
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:]
            stringline += currentPlace
            # add item to the list
            if count == 17:
                r_lst_ref.append(stringline)
                count = 0
                stringline = ""
            count += 1
    return r_lst_ref


def extract_number(text):

    p = re.compile(r'[+]*\d+[\s]*\d*[\s]*\d*[\s]*\d+')
    lst = text.split("\n")
    for j in lst:
        if "." in j: continue 
        x = p.findall(j)
        if len(x) > 0: cool = x
        
    temp = ""
    try:
        temp = temp.join(cool)
    except:
        return temp    
    return temp
    


def main():
    # text = "Uli Dersen \n\n© Zutriedenheit: TOP ® Zuverlassig \n Privater Nutzer \n \n Aktiv seit 03.04.2015 \n eo 0175-2252627 \n 9 Anzeigen online % Folgen \n A\ Ameige melden\n © Anzeige drucken"
    # x = re.findall(".\d*\n$", text)
    data = data_read_lst()
    # print(data)
    final_numbers = []
    for i in data:
        # print(i)
        
        temp = extract_number(i)
        print(temp)
        final_numbers.append(temp)
        # break
    print(final_numbers)


main()