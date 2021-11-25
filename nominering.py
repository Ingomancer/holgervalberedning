import csv
import os
import sys
import smtplib
from email.message import EmailMessage

valberedningen = "Test1 och Test2"
deadline = "en dag (ett datum)"
svarsmail = "mail@mail.mail"
tjatdag = "nåndag"
nomineringsfil = "ExempelNomineringar.csv"
mail_dir = "mail"
mail_user = "mail@mail.mail"
mail_password = 'NOPE'
mail_service = 'smtp.gmail.com'

mail_template = """\
Hej​! ​

Nu har vi sammanställt nomineringarna och du har blivit nominerad till följande poster:

{poster}

Vi vill att du tar och funderar på hur du ställer dig till nomineringarna. Senast​ {deadline} behöver vi veta ditt svar per nominering (ja, nej, kanske). Väljer du att skriva kanske så vill vi ha en förklaring tex: Behöver få reda på om jag har fått det där extrajobbet jag sökte först.

Du svarar genom att maila till mig eller {svarsmail} när du väl har tagit ställning och har sagt ja till en eller flera nomineringar

Är du sugen på en eller flera poster så vill vi ha in en motivering till varför du skulle passa bra på just den posten. Detta för att vi ska ha lite mer på fötterna när vi ska arbeta med att ta fram vårt förslag till årsmötet.

​Vi kommer att ringa runt på {tjatdag}, och därför är det bra om du har telefonen i närheten då. Det är också jättebra att meddela oss om du vet att du inte kommer vara kontaktbar på {tjatdag}. ​

Vad händer sen

    Vi i valberedningen kommer sätta oss ned och diskutera fram och tillbaka och lägga fram ett förslag till årsmötet.
    När vi har fått fram vårt förslag så kommer vi att ringa er som vi vill föreslå samt er som ​sagt ja/kanske som ​vi inte kommer föreslå så att ni har möjlighet att motkandidera om ni vill.
    På årsmötet kommer hela föreningen att bestämma om ni blir valda eller ej och vem som helst kan motkandidera till de olika posterna.

Här är en länk till Holgerspexets policydokument, där de flesta ansvarsposterna är beskrivna: https://insidan.holgerspexet.se/arkivet/#/Styrdokument/

Har du någon fråga eller fundering så är det bara att ringa eller maila oss, kontaktuppgifter finns på insidan.

Enorma kramar från {valberedningen}"""

def generate_emails():
    with open (nomineringsfil, encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile)
        nomineringar = {}
        for line in reader:
            try:
                nomineringar[(line[2], line[4])].add(line[1])
            except KeyError:
                nomineringar[(line[2], line[4])] = set()
                nomineringar[(line[2], line[4])].add(line[1])
        os.makedirs('mail', exist_ok=True)
        for (namn, email), poster in nomineringar.items():
            with open(f'{mail_dir}/{email}', 'w', encoding='UTF-8') as output:
                output.write(mail_template.format(poster="\n".join(poster), deadline=deadline, svarsmail=svarsmail, tjatdag=tjatdag, valberedningen=valberedningen))

def send_emails():
    server = smtplib.SMTP_SSL(mail_service, 465)
    server.ehlo()
    server.login(mail_user, mail_password)
    for filename in os.listdir(mail_dir):
        mail = filename
        with open(f"{mail_dir}/{filename}", 'r', encoding="UTF-8") as f:
            content = f.read()
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = "Du har blivit nominerad!"
        msg['From'] = mail_user
        msg['To'] = mail
        server.send_message(msg)
    server.close

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'mail':
        send_emails()
    else:
        generate_emails()