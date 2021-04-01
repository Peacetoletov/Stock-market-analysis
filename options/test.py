"""
Hypotéza je taková, že když jeden měsíc šla cena nahoru, tak je vysoká
šance, že následující měsíc půjde taky nahoru. Stejně tak pokud tento měsíc
šla cena dolů, je vysoká šance, že příští měsíc půjde taky dolů.

První hypotéza je tedy binární - dívám se jen na směr ceny, nikoliv jak moc
se cena změnila. Druhá hypotéza tvrdí, že velkému poklesu (>10% nebo >20%)
předcházel malý pokles (>0%). Chci se tedy podívat na všechny velké poklesy
a zjistit, kolika z nich skutečně předcházel malý pokles

Options trading strategie:
Vyberu akcii, která za poslední měsíc vzrostla. Prodám put s expirací za
měsíc a se strike price = 0.95 aktuální hodnoty. Dokoupím put s menší strike
price, abych měl vertical put spread. Cílím na premium x, maximální ztrátu 5x.

Chci otestovat, jak efektivní tato strategie bude. Testovat budu na S&P 500
společnostech z roku 2000.
Update: Zjistil jsem, že spousta společností byla vyřazena z S&P 500 ne
proto, že by zbankrotovaly, ale proto, že šly private. Proto si nemyslím,
že bude moc velký rozdíl, když použiju aktuální S&P 500 společnosti. Pokud
se budu chtít trochu vyvarovat survivorship biasu, můžu brát jenom data od
roku 2010. 120 měsíců * 500 firem = 60 000 sample size -> good.
"""

"""
1. Stáhnout S&P 500 firmy s časovým rozestupem 1 měsíc.
2. Procházet jednu po druhé a dívat se, jestli platí hypotéza, že po zelené 
bývá zelená, po červené červená.
3. Otestovat, jak by fungovala options strategie.
"""