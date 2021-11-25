Om man tar in nomineringar via google forms, på formatet:
```
Vilken ansvarspost?
Vem?
Varför?
```
och sedan fyller i folks mailadresser och exporterar som csv, kan det här scriptet generera alla nomineringsmail:
```
python3 nominering.py
```
vilket skapar katalogen "mail" med ett mail per person. Kontrollera dessa så det ser rätt ut!
Sedan kan man skicka alla mail:
```
python3 nominering.py mail
```
vilket automatiskt skickar alla mail, om man angett en giltig mail/lösenords-kombo. 
För gmail behöver man använda ett app password istället för sitt vanliga, se: https://support.google.com/accounts/answer/185833?hl=en
