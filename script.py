import email
from email import policy
from email.parser import BytesParser
import os


#### FUNCTION TO CHECK IS HEADER A MAIL ADDRESS OR NOT:
def checkHead(headerName, headerbodyname, headerbody, dct):
    if headerbodyname == headerName:
        dct[headerName.lower()]=headerbody
    else:
        pass

#### STRUCTURE: MAIL ADDRESS IS A KEY, AND EACH KEY HAS 6 VALUES:
email_dict = dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
emails = {}


with open('results.txt', "w") as results:
    for file in os.listdir('./msgs'):
        with open('./msgs/{}'.format(file), 'rb') as msg_file:  # select a specific email file from the list
            msg = BytesParser(policy=policy.default).parse(msg_file)
        for header in msg._headers:
            if header[0] == "Subject":
                subject = header[1].replace("\n", "")
                decoded = email.header.decode_header(subject)
                subject_decoded = decoded[0][0].decode(decoded[0][1])

########################################################################################################################
#### PART "delivered" is not the same as other parts                                                             ####
########################################################################################################################
#### PARSING MESSAGES THAT WERE DELIVERED, EXTRACTING MAIL ADDRESS FROM MAIL BODY AND WRITE INTO THE DICTIONARY  ####
#######################################################################################################################
                if "delivered" in subject_decoded.lower():
                    text = msg.get_body(preferencelist=('plain')).get_content()
                    splitted_text = text.replace("\n\n", "\n").split("\n")
                    delivered_address = "<" + splitted_text[1][:splitted_text[1].find('<')] + ">"
                    for head_delivered_a in msg._headers:
                        if delivered_address not in emails:
                            emails[delivered_address]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                        for head_delivered_b in msg._headers:
                            checkHead("Date",head_delivered_b[0],head_delivered_b[1],emails[delivered_address])
                            if emails[delivered_address]["date"]!=None:
                                emails[delivered_address]["delivery_status"]="True"
                                emails[delivered_address]["subject"]=subject_decoded
                    #pass

########################################################################################################################
# DELIVERED REPLY
########################################################################################################################
                elif "read" in subject_decoded.lower():
                    for head_read_a in msg._headers:
                        if head_read_a[0] == "Return-Path":
                            curr_email = head_read_a[1]
                            if curr_email not in emails:
                                emails[head_read_a[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            for head_read_b in msg._headers:
                                checkHead("Date",head_read_b[0],head_read_b[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["opening_status"]="True"
                                    emails[curr_email]["subject"]=subject_decoded

                elif "прочтено:" in subject_decoded.lower():
                    for head_proc in msg._headers:
                        if head_proc[0] == "Return-Path":
                            curr_email = head_proc[1]
                            if curr_email not in emails:
                                emails[head_proc[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            for head_proc in msg._headers:
                                checkHead("Date",head_proc[0],head_proc[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["opening_status"]="True"
                                    emails[curr_email]["subject"]=subject_decoded

########################################################################################################################
#  REAL REPLY
########################################################################################################################
                elif "re:" in subject_decoded.lower():
                    for head_re_a in msg._headers:
                         if head_re_a[0] == "Return-Path":
                            emails[head_re_a[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            curr_email = head_re_a[1]
                            for head_re_b in msg._headers:
                                checkHead("Date",head_re_b[0],head_re_b[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["reply"]="True"
                                    emails[curr_email]["subject"]=subject_decoded


########################################################################################################################
# HOLIDAY REPLY
########################################################################################################################
                elif "автоматический" in subject_decoded.lower():
                    for head_hol_a in msg._headers:
                         if head_hol_a[0] == "Return-Path":
                            emails[head_hol_a[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            curr_email = head_hol_a[1]
                            for head_hol_b in msg._headers:
                                checkHead("Date",head_hol_b[0],head_hol_b[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["holiday"]="True"
                                    emails[curr_email]["subject"]=subject_decoded


                elif "automatic" in subject_decoded.lower():
                    for head_hol_a in msg._headers:
                         if head_hol_a[0] == "Return-Path":
                            emails[head_hol_a[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            curr_email = head_hol_a[1]
                            for head_hol_b in msg._headers:
                                checkHead("Date",head_hol_b[0],head_hol_b[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["holiday"]="True"
                                    emails[curr_email]["subject"]=subject_decoded
                                    
########################################################################################################################
# HOLIDAY REPLY
########################################################################################################################
                elif "не прочтено:" in subject_decoded.lower():
                    for head_not_re_a in msg._headers:
                         if head_not_re_a[0] == "Return-Path":
                            emails[head_not_re_a[1]]=dict.fromkeys(['subject','date','delivery_status','opening_status','reply','holiday','notread'])
                            curr_email = head_not_re_a[1]
                            for head_not_re_b in msg._headers:
                                checkHead("Date",head_not_re_b[0],head_not_re_b[1],emails[curr_email])
                                if emails[curr_email]["date"]!=None:
                                    emails[curr_email]["notread"]="True"

                else:
                    pass
                    #os.rename(msg_file.name, "./unparsed/{}".format(file))
                    #shutil.move(msg_file.name, "/unparsed/{}".format(ile.name))

#for key in emails:
#    emails[key]["subject"] = emails[key]["subject"][emails[key]["subject"].find(':')+2:]
    #emails[key] = emails[key]
for key in emails:
    print(key, emails[key])




#     for head_delivered in msg._headers:
#         if head_delivered[0] == "Return-Path":
#             emails[head_delivered[1]] = email_dict
#             curr_email = head_delivered[1]
#     if head_delivered[0] == "Return-Path":
#         emails[head_delivered[1]]=email_dict
#         curr_email=head_delivered[1]

#     if "delivered" in status:
#         results.write("Status: {0}, Address: {1}".format(splitted_text[0], splitted_text[1]))
#         text = msg.get_body(preferencelist=('plain')).get_content()
#         splitted_text = text.replace("\n\n", "\n").split("\n")







