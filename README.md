## MIP-1-praktiskais darbs

## Papildu prasības programmatūrai 

# Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas skaitļu virknes garumu, kas var būt diapazonā no 15 līdz 25 skaitļiem. Spēles programmatūra gadījuma ceļā  saģenerē skaitļu virkni atbilstoši uzdotajam garumam, tajā iekļaujot skaitļus no 1 līdz 9. 

_Spēles apraksts_ 

Spēles sākumā ir dota ģenerētā skaitļu virkne. Kopīgs punktu skaits ir 0 (šajā spēlē punkti netiek skaitīti katram spēlētājam atsevišķi). Spēlē arī tiek izmantota banka, kura sākotnēji vienāda ar 0. Spēlētāji izpilda gājienus secīgi. Gājiena laikā spēlētājs aizvieto jebkuru skaitļu pāri (divus blakus stāvošus skaitļus), pamatojoties uz šādiem principiem: 

ja divu blakus stāvošu skaitļu summa ir lielāka par 7, tad skaitļu pāri aizvieto ar 1 un kopīgajam punktu skaitam pieskaita 1 punktu; 

ja divu blakus stāvošu skaitļu summa ir mazāka par 7, tad skaitļu pāri aizvieto ar 3 un no kopīgā punktu skaita atņem 1 punktu; 

ja divu blakus stāvošu skaitļu summa ir vienāda ar 7, tad skaitļu pāri aizvieto ar 2 un spēles bankai pieskaita 1 punktu. 

Spēle beidzas, kad skaitļu virknē paliek tikai viens skaitlis. Ja gan bankas punktu skaits, gan kopīgais punktu skaits ir pāra skaitlis, tad uzvar spēlētājs, kurš uzsāka spēli. Ja gan bankas punktu skaits, gan kopīgais punktu skaits ir nepāra skaitlis, tad uzvar otrais spēlētājs. Visos citos gadījumos ir neizšķirts rezultāts. 
